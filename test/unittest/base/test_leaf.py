import dataclasses as dc
import typing as t
from pprint import pprint

from superduperdb import ObjectModel
from superduperdb.backends.mongodb.query import MongoQuery
from superduperdb.base.document import Document
from superduperdb.base.leaf import Leaf
from superduperdb.base.variables import Variable
from superduperdb.components.component import Component
from superduperdb.components.datatype import _BaseEncodable
from superduperdb.components.listener import Listener


@dc.dataclass
class Test(Leaf):
    b: t.Optional[t.Union[str, Variable]] = 'a'
    c: t.Optional[t.Union[float, Variable]] = 1.0
    a: t.Optional[int] = 1


@dc.dataclass
class OtherSer(Leaf):
    d: str = 'd'


@dc.dataclass(kw_only=True)
class TestSubModel(Component):
    type_id: t.ClassVar[str] = 'test-sub-model'
    a: int = 1
    b: t.Union[str, Variable] = 'b'
    c: ObjectModel = dc.field(
        default_factory=ObjectModel(identifier='test-2', object=lambda x: x + 2)
    )
    d: t.List[ObjectModel] = dc.field(default_factory=[])
    e: OtherSer = dc.field(default_factory=OtherSer(identifier='test', d='test'))
    f: t.Callable = dc.field(default=lambda x: x)


@dc.dataclass
class MySer(Leaf):
    a: int = 1
    b: str = 'b'
    c: Leaf = dc.field(default_factory=OtherSer(identifier='test', d='test'))


def test_encode_leaf():
    obj = Test('test', a=1, b='test_b', c=1.5)
    assert obj.dict().encode() == {
        '_path': 'test/unittest/base/test_leaf/Test',
        'uuid': obj.uuid,
        'identifier': 'test',
        'a': 1,
        'b': 'test_b',
        'c': 1.5,
        '_leaves': {},
        '_files': {},
        '_blobs': {},
    }


def test_no_wrap():
    m = Listener(
        key='X',
        model=ObjectModel(
            identifier='test',
            object=lambda x: x + 2,
        ),
        select=None,
    )

    r = m.encode(leaves_to_keep=(_BaseEncodable,))

    decoded = Document.decode(r).unpack()
    decoded.init()
    print(decoded)


def test_encode_leaf_with_children():
    obj = MySer(
        identifier='my_ser',
        a=1,
        b='test_b',
        c=OtherSer(identifier='other_ser', d='test'),
    )
    assert obj.dict().encode() == {
        '_path': 'test/unittest/base/test_leaf/MySer',
        'uuid': obj.uuid,
        'identifier': 'my_ser',
        'a': 1,
        'b': 'test_b',
        'c': obj.c.dict().unpack(),
        '_leaves': {},
        '_files': {},
        '_blobs': {},
    }


def test_save_variables_2():
    query = (
        MongoQuery('documents')
        .like({'x': Variable('X')}, vector_index='test')
        .find({'x': {'$regex': '^test/1'}})
    )

    assert [x.value for x in query.variables] == ['X']


def test_saveable():
    s = MySer(identifier='sr', a=1, b='test', c=OtherSer(identifier='other', d='test'))
    r = Document(s.dict()).encode()
    print(r)


def test_component_with_document():
    t = TestSubModel(
        identifier='test-1',
        a=2,
        b='test',
        c=ObjectModel('test-2', object=lambda x: x + 2),
        d=[ObjectModel('test-3', object=lambda x: x + 2)],
        e=OtherSer(identifier='other', d='test'),
        f=lambda x: x,
    )
    print('encoding')
    d = Document(t.dict())
    r = d.encode()
    leaves = r['_leaves']

    pprint(r)
    assert len(leaves) == 7

    for leaf in leaves:
        print(type(leaf))


def test_find_variables():
    from superduperdb import Document
    from superduperdb.backends.mongodb import MongoQuery
    from superduperdb.base.variables import Variable

    r = Document({'txt': Variable('test')})

    assert [str(x) for x in r.variables] == ['?test']

    q = MongoQuery('test').find_one(Document({'txt': Variable('test')}))

    assert [str(x) for x in q.variables] == ['?test']

    q = (
        MongoQuery('test')
        .like(Document({'txt': Variable('test')}), vector_index='test')
        .find()
        .limit(5)
    )

    q_set = q.set_variables(None, test='my-value')

    assert q_set.variables == []
