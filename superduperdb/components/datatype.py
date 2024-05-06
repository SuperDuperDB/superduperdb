import base64
import dataclasses as dc
import hashlib
import inspect
import io
import os
import pickle
import re
import typing as t
from abc import abstractmethod

import dill

from superduperdb import CFG
from superduperdb.backends.base.artifacts import (
    ArtifactSavingError,
    _construct_file_id_from_uri,
)
from superduperdb.base.config import BytesEncoding
from superduperdb.base.leaf import Leaf
from superduperdb.components.component import Component, ensure_initialized
from superduperdb.misc.annotations import component, public_api
from superduperdb.misc.hash import random_sha1

Decode = t.Callable[[bytes], t.Any]
Encode = t.Callable[[t.Any], bytes]

if t.TYPE_CHECKING:
    from superduperdb.base.datalayer import Datalayer


class Empty:
    def __repr__(self):
        return '<EMPTY>'


def pickle_encode(object: t.Any, info: t.Optional[t.Dict] = None) -> bytes:
    return pickle.dumps(object)


def pickle_decode(b: bytes, info: t.Optional[t.Dict] = None) -> t.Any:
    return pickle.loads(b)


def dill_encode(object: t.Any, info: t.Optional[t.Dict] = None) -> bytes:
    return dill.dumps(object, recurse=True)


def dill_decode(b: bytes, info: t.Optional[t.Dict] = None) -> t.Any:
    return dill.loads(b)


def file_check(path: t.Any, info: t.Optional[t.Dict] = None) -> str:
    if not (isinstance(path, str) and os.path.exists(path)):
        raise ValueError(f"Path '{path}' does not exist")
    return path


def torch_encode(object: t.Any, info: t.Optional[t.Dict] = None) -> bytes:
    import torch

    from superduperdb.ext.torch.utils import device_of

    if not isinstance(object, dict):
        previous_device = str(device_of(object))
        object.to('cpu')
        f = io.BytesIO()
        torch.save(object, f)
        object.to(previous_device)
    else:
        f = io.BytesIO()
        torch.save(object, f)
    return f.getvalue()


def torch_decode(b: bytes, info: t.Optional[t.Dict] = None) -> t.Any:
    import torch

    return torch.load(io.BytesIO(b))


def to_base64(bytes):
    return base64.b64encode(bytes).decode('utf-8')


def from_base64(encoded):
    return base64.b64decode(encoded)


@public_api(stability='stable')
@dc.dataclass(kw_only=True)
class DataType(Component):
    """
    {component_parameters}
    :param identifier: Unique identifier
    :param decoder: callable converting a ``bytes`` string to a ``Encodable``
                    of this ``Encoder``
    :param encoder: Callable converting an ``Encodable`` of this ``Encoder``
                    to ``bytes``
    :param shape: Shape of the data
    :param load_hybrid: Whether to load the data from the URI or return the URI in
                        `CFG.hybrid` mode
    """

    __doc__ = __doc__.format(component_parameters=Component.__doc__)

    ui_schema: t.ClassVar[t.List[t.Dict]] = [
        {
            'name': 'serializer',
            'type': 'string',
            'choices': ['pickle', 'dill', 'torch'],
            'default': 'dill',
        },
        {'name': 'info', 'type': 'json', 'optional': True},
        {'name': 'shape', 'type': 'json', 'optional': True},
        {'name': 'directory', 'type': 'str', 'optional': True},
        {
            'name': 'encodable',
            'type': 'str',
            'choices': ['encodable', 'lazy_artifact', 'file'],
            'default': 'lazy_artifact',
        },
        {
            'name': 'bytes_encoding',
            'type': 'str',
            'choices': ['base64', 'bytes'],
            'default': 'bytes',
        },
        {'name': 'media_type', 'type': 'str', 'optional': True},
    ]

    type_id: t.ClassVar[str] = 'datatype'
    encoder: t.Optional[t.Callable] = None  # not necessary if encodable is file
    decoder: t.Optional[t.Callable] = None
    info: t.Optional[t.Dict] = None
    shape: t.Optional[t.Sequence] = None
    directory: t.Optional[str] = None
    encodable: str = 'encodable'
    bytes_encoding: t.Optional[str] = CFG.bytes_encoding
    media_type: t.Optional[str] = None

    def __post_init__(self, db, artifacts):
        self._encodable_cls = _ENCODABLES[self.encodable]
        super().__post_init__(db, artifacts)
        self.bytes_encoding = self.bytes_encoding or CFG.bytes_encoding

    def dict(self):
        r = super().dict()
        if hasattr(self.bytes_encoding, 'value'):
            r['bytes_encoding'] = str(self.bytes_encoding.value)
        return r

    def __call__(
        self, x: t.Optional[t.Any] = None, uri: t.Optional[str] = None
    ) -> '_BaseEncodable':
        return self._encodable_cls(datatype=self, x=x, uri=uri)

    @ensure_initialized
    def encode_data(self, item, info: t.Optional[t.Dict] = None):
        info = info or {}
        data = self.encoder(item, info)
        data = self.bytes_encoding_after_encode(data)
        return data

    @ensure_initialized
    def decode_data(self, item, info: t.Optional[t.Dict] = None):
        info = info or {}
        item = self.bytes_encoding_before_decode(item)
        return self.decoder(item, info=info)

    def bytes_encoding_after_encode(self, data):
        if self.bytes_encoding == BytesEncoding.BASE64:
            return to_base64(data)
        return data

    def bytes_encoding_before_decode(self, data):
        if self.bytes_encoding == BytesEncoding.BASE64:
            return from_base64(data)
        return data


def encode_torch_state_dict(module, info):
    import torch

    buffer = io.BytesIO()
    torch.save(module.state_dict(), buffer)

    return buffer.getvalue()


class DecodeTorchStateDict:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, b: bytes, info: t.Dict):
        import torch

        buffer = io.BytesIO(b)
        module = self.cls(**info)
        module.load_state_dict(torch.load(buffer))
        return module


def build_torch_state_serializer(module, info):
    return DataType(
        identifier=module.__name__,
        info=info,
        encoder=encode_torch_state_dict,
        decoder=DecodeTorchStateDict(module),
    )


def _find_descendants(cls):
    descendants = cls.__subclasses__()
    for subclass in descendants:
        descendants.extend(_find_descendants(subclass))
    return descendants


@dc.dataclass(kw_only=True)
class _BaseEncodable(Leaf):
    """
    Data variable wrapping encode-able item. Encoding is controlled by the referred
    to ``Encoder`` instance.

    :param encoder: Instance of ``Encoder`` controlling encoding
    :param x: Wrapped content
    :param uri: URI of the content, if any
    """

    identifier: str = ''
    file_id: t.Optional[str] = None
    datatype: DataType
    uri: t.Optional[str] = None
    sha1: t.Optional[str] = None
    x: t.Optional[t.Any] = None

    def __post_init__(self, db):
        super().__post_init__(db)
        if self.uri is not None and self.file_id is None:
            self.file_id = _construct_file_id_from_uri(self.uri)

        if self.uri and not re.match('^[a-z]{0,5}://', self.uri):
            self.uri = f'file://{self.uri}'

    @property
    def id(self):
        assert self.file_id is not None
        return f'{self.leaf_type}/{self.file_id}'

    @property
    def reference(self):
        return self.datatype.reference

    def unpack(self):
        """
        Unpack the content of the `Encodable`

        :param db: `Datalayer` instance to assist with
        """
        return self.x

    @classmethod
    def get_encodable_cls(cls, name, default=None):
        """
        Get the subclass of the _BaseEncodable with the given name.
        All the registered subclasses must be subclasses of the _BaseEncodable.
        """
        for sub_cls in _find_descendants(cls):
            if sub_cls.__name__.lower() == name.lower().replace('_', '').replace(
                '-', ''
            ):
                return sub_cls
        if default is None:
            raise ValueError(f'No subclass with name "{name}" found.')
        elif not issubclass(default, cls):
            raise ValueError(
                "The default class must be a subclass of the _BaseEncodable."
            )
        return default

    def get_hash(self, data):
        if isinstance(data, str):
            bytes_ = data.encode()
        elif isinstance(data, bytes):
            bytes_ = data
        else:
            raise ValueError(f'Unsupported data type: {type(data)}')
        return hashlib.sha1(bytes_).hexdigest()


@dc.dataclass
class Encodable(_BaseEncodable):
    x: t.Any = Empty()
    blob: dc.InitVar[t.Optional[bytearray]] = None
    leaf_type: t.ClassVar[str] = 'encodable'

    def __post_init__(self, db, blob):
        super().__post_init__(db)
        if isinstance(self.x, Empty):
            self.datatype.init()
            self.x = self.datatype.decoder(blob)

    def _encode(self):
        bytes_ = self.datatype.encode_data(self.x)
        sha1 = self.get_hash(bytes_)
        return bytes_, sha1

    def _deep_flat_encode(self, cache, blobs, files, leaves_to_keep=()):
        if isinstance(self, leaves_to_keep):
            cache[self.id] = self
            return f'?{self.id}'

        maybe_bytes, file_id = self._encode()
        self.file_id = file_id
        r = super()._deep_flat_encode(cache, blobs, files)
        del r['x']
        r['blob'] = maybe_bytes
        cache[self.id] = r
        return f'?{self.id}'

    @classmethod
    def _get_object(cls, db, r):
        if r.get('bytes') is None:
            return None
        if db is None:
            try:
                from superduperdb.components.datatype import serializers

                datatype = serializers[r['datatype']]
            except KeyError:
                raise Exception(
                    f'You specified a serializer which doesn\'t have a'
                    f' default value: {r["datatype"]}'
                )
        else:
            datatype = db.datatypes[r['datatype']]
        object = datatype.decode_data(r['bytes'], info=datatype.info)
        return object

    @classmethod
    def build(cls, r):
        return cls(**r)

    def init(self, db):
        pass


@dc.dataclass
class Native(_BaseEncodable):
    """
    Native data supported by underlying database
    """

    leaf_type: t.ClassVar[str] = 'native'
    x: t.Optional[t.Any] = None

    @classmethod
    def _get_object(cls, db, r):
        raise NotImplementedError

    def _deep_flat_encode(self, cache, blobs, files, leaves_to_keep=()):
        if isinstance(self, leaves_to_keep):
            cache[self.id] = self
            return f'?{self.id}'

        r = super()._deep_flat_encode(cache, blobs, files)
        cache[self.id] = r
        return f'?{self.id}'


class _ArtifactSaveMixin:
    def save(self, artifact_store):
        r = artifact_store.save_artifact(self.encode()['_content'])
        self.x = None
        self.file_id = r['file_id']


@dc.dataclass
class Artifact(_BaseEncodable, _ArtifactSaveMixin):
    """
    Data to be saved on disk/ in the artifact-store
    """

    leaf_type: t.ClassVar[str] = 'artifact'
    x: t.Any = Empty()
    lazy: t.ClassVar[bool] = False

    def __post_init__(self, db):
        super().__post_init__(db)

        if not self.lazy and isinstance(self.x, Empty):
            self.init()

        if self.datatype.bytes_encoding == BytesEncoding.BASE64:
            raise ArtifactSavingError('BASE64 not supported on disk!')

    def init(self):
        assert self.file_id is not None
        if isinstance(self.x, Empty):
            blob = self.db.artifact_store._load_bytes(self.file_id)
            self.datatype.init()
            self.x = self.datatype.decoder(blob)

    def _deep_flat_encode(self, cache, blobs, files, leaves_to_keep=()):
        if isinstance(self, leaves_to_keep):
            cache[self.id] = self
            return f'?{self.id}'

        maybe_bytes, file_id = self._encode()
        self.file_id = file_id
        r = super()._deep_flat_encode(cache, blobs, files, leaves_to_keep=leaves_to_keep)
        del r['x']
        blobs[self.file_id] = maybe_bytes
        cache[self.id] = r
        return f'?{self.id}'

    def _encode(self):
        bytes_ = self.datatype.encode_data(self.x)
        sha1 = self.get_hash(bytes_)
        return bytes_, sha1

    def unpack(self):
        """
        Unpack the content

        :param db: `Datalayer` instance to assist with
        """
        self.init()
        return self.x


@dc.dataclass
class LazyArtifact(Artifact):
    """
    Data to be saved on disk/ in the artifact-store
    """

    leaf_type: t.ClassVar[str] = 'lazy_artifact'
    lazy: t.ClassVar[bool] = True


@dc.dataclass
class File(_BaseEncodable, _ArtifactSaveMixin):
    """
    Data to be saved on disk and passed
    as a file reference
    """

    leaf_type: t.ClassVar[str] = 'file'
    x: t.Any = Empty()

    def _deep_flat_encode(self, cache, blobs, files, leaves_to_keep=()):
        if isinstance(self, leaves_to_keep):
            cache[self.id] = self
            return f'?{self.id}'

        self.file_id = self.file_id or random_sha1()
        if self.x not in files:
            files.append(self.x)
        return f'?{self.id}'

    def init(self, db):
        if isinstance(self.x, Empty):
            file = db.artifact_store._load_file(self.file_id)
            self.x = file

    def unpack(self):
        self.init()
        return self.x

    @classmethod
    def _get_object(cls, db, r):
        return r['x']

    @classmethod
    def decode(cls, r, db=None) -> 'File':
        file = cls(
            x=Empty(),
            datatype=db.datatypes[r['_content']['datatype']],
            file_id=r['_content']['file_id'],
        )
        file.init(db)
        return file


class LazyFile(File):
    leaf_type: t.ClassVar[str] = 'lazy_file'

    @classmethod
    def decode(cls, r, db=None) -> 'LazyFile':
        file = cls(
            x=Empty(),
            datatype=db.datatypes[r['_content']['datatype']],
            file_id=r['_content']['file_id'],
        )
        return file


Encoder = DataType


_ENCODABLES = {
    'encodable': Encodable,
    'artifact': Artifact,
    'lazy_artifact': LazyArtifact,
    'file': File,
    'native': Native,
    'lazy_file': LazyFile,
}


methods = {
    'pickle': {'encoder': pickle_encode, 'decoder': pickle_decode},
    'dill': {'encoder': dill_encode, 'decoder': dill_decode},
    'torch': {'encoder': torch_encode, 'decoder': torch_decode},
    'file': {'encoder': file_check, 'decoder': file_check},
}


@component()
def get_serializer(identifier: str, method: str, encodable: str, db: t.Optional['Datalayer'] = None):
    return DataType(
        identifier=identifier,
        encodable=encodable,
        **methods[method],
        db=db,
    )


pickle_encoder = get_serializer(
    identifier='pickle',
    method='pickle',
    encodable='encodable',
)


pickle_serializer = get_serializer(
    identifier='pickle',
    method='pickle',
    encodable='artifact',
)

pickle_lazy = get_serializer(
    identifier='pickle_lazy',
    method='pickle',
    encodable='lazy_artifact',
)

dill_serializer = get_serializer(
    identifier='dill',
    method='dill',
    encodable='artifact',
)

dill_lazy = get_serializer(
    identifier='dill_lazy',
    method='dill',
    encodable='lazy_artifact',
)

torch_serializer = get_serializer(
    identifier='torch',
    method='torch',
    encodable='lazy_artifact',
)

file_serializer = get_serializer(
    identifier='file',
    method='file',
    encodable='file',
)

file_lazy = get_serializer(
    identifier='file_lazy',
    method='file',
    encodable='lazy_file',
)

serializers = {
    'pickle': pickle_serializer,
    'dill': dill_serializer,
    'torch': torch_serializer,
    'file': file_serializer,
    'pickle_lazy': pickle_lazy,
    'dill_lazy': dill_lazy,
    'file_lazy': file_lazy,
}
