import re
import signal
import sys
import typing as t
import warnings
from contextlib import contextmanager
from io import BytesIO
from multiprocessing.pool import ThreadPool

import boto3
import requests

from superduperdb.misc.logger import logging
from superduperdb.misc.progress import progressbar


class TimeoutException(Exception):
    ...


def timeout_handler(signum: t.Any, frame: t.Callable):  # pragma: no cover
    raise TimeoutException()


@contextmanager
def timeout(seconds: int):  # pragma: no cover
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


class Fetcher:
    def __init__(self, headers: t.Optional[int] = None, n_workers: int = 0) -> None:
        session = boto3.Session()
        self.headers = headers
        self.s3_client = session.client("s3")
        self.request_session = requests.Session()
        self.request_adapter = requests.adapters.HTTPAdapter(
            max_retries=3,
            pool_connections=n_workers if n_workers else 1,
            pool_maxsize=n_workers * 10,
        )
        self.request_session.mount("http://", self.request_adapter)
        self.request_session.mount("https://", self.request_adapter)

    def _download_s3_object(self, uri: str) -> bytes:
        f = BytesIO()
        path = uri.split('s3://')[-1]
        bucket_name = path.split('/')[0]
        file = '/'.join(path.split('/')[1:])
        self.s3_client.download_fileobj(bucket_name, file, f)
        return f.getvalue()

    def _download_file(self, path: str) -> t.AnyStr:
        path = re.split('^file://', path)[-1]
        with open(path, 'rb') as f:
            return f.read()

    def _download_from_uri(self, uri: str) -> bytes:
        return self.request_session.get(uri, headers=self.headers).content

    def __call__(self, uri: str) -> bytes:
        if uri.startswith('file://'):
            return self._download_file(uri)
        elif uri.startswith('s3://'):
            return self._download_s3_object(uri)
        elif uri.startswith('http://') or uri.startswith('https://'):
            return self._download_from_uri(uri)
        else:
            raise NotImplementedError(f'unknown type of URI "{uri}"')


class BaseDownloader:
    def __init__(
        self,
        uris: t.List[str],
        n_workers: int = 0,
        timeout: t.Any = None,
        headers: t.Optional[int] = None,
        raises: bool = True,
    ) -> None:
        self.timeout = timeout
        self.n_workers = n_workers
        self.uris = uris
        self.headers = headers or {}
        self.raises = raises

    def go(self) -> None:
        """
        Download all files
        Uses a :py:class:`multiprocessing.pool.ThreadPool` to parallelize
                          connections.
        :param test: If *True* perform a test run.
        """
        logging.info(f'number of workers {self.n_workers}')
        prog = progressbar(total=len(self.uris))
        prog.prefix = 'downloading from uris'
        self.failed = 0
        prog.prefx = "failed: 0"

        def f(i: int) -> None:
            prog.update()
            try:
                if self.timeout is not None:  # pragma: no cover
                    with timeout(self.timeout):
                        self._download(i)
                else:
                    self._download(i)
            except TimeoutException:  # pragma: no cover
                logging.warning(f'timed out {i}')
            except KeyboardInterrupt:  # pragma: no cover
                raise
            except Exception as e:  # pragma: no cover
                if self.raises:
                    raise e
                warnings.warn(str(e))
                self.failed += 1
                prog.prefix = f"failed: {self.failed} [{e}]"

        if self.n_workers == 0:
            self._sequential_go(f)
            return

        self._parallel_go(f)

    def _parallel_go(self, f: t.Callable) -> None:
        pool = ThreadPool(self.n_workers)
        try:
            pool.map(f, range(len(self.uris)))
        except KeyboardInterrupt:  # pragma: no cover
            logging.warning("--keyboard interrupt--")
            pool.terminate()
            pool.join()
            sys.exit(1)

        pool.close()
        pool.join()

    def _sequential_go(self, f: t.Callable) -> None:
        for i in range(len(self.uris)):
            f(i)


class Downloader(BaseDownloader):
    """

    :param uris: list of uris/ file names to fetch
    :param update_one: function to call to insert data into table
    :param ids: list of ids of rows/ documents to update
    :param keys: list of keys in rows/ documents to insert to
    :param n_workers: number of multiprocessing workers
    :param raises: raises error ``True``/``False``
    :param headers: dictionary of request headers passed to``requests`` package
    :param skip_existing: if ``True`` then don't bother getting already present data
    :param timeout: set seconds until request times out
    """

    results: t.Dict[int, str]

    def __init__(
        self,
        uris,
        update_one=None,
        ids=None,
        keys=None,
        n_workers=20,
        headers=None,
        skip_existing=True,
        timeout=None,
        raises=True,
    ) -> None:
        super().__init__(
            uris, n_workers=n_workers, timeout=timeout, headers=headers, raises=raises
        )
        self.ids = ids
        self.keys = keys
        self.failed = 0
        self.skip_existing = skip_existing
        self.update_one = update_one
        self.fetcher = Fetcher(headers=headers, n_workers=n_workers)

        assert len(ids) == len(uris)

    def _download(self, i: int) -> None:
        uri = self.uris[i]
        _id = self.ids[i]
        content = self.fetcher(uri)
        self.update_one(self.ids[i], self.keys[i], content)


class InMemoryDownloader(BaseDownloader):
    def __init__(
        self,
        *args: t.Any,
        headers: t.Optional[int] = None,
        n_workers: int = 0,
        **kwargs: t.Dict[str, t.Any],
    ) -> None:
        super().__init__(*args, **kwargs)
        self.results = {}
        self.fetcher = Fetcher(headers=headers, n_workers=n_workers)

    def _download(self, i: int) -> None:
        content = self.fetcher(self.uris[i])
        self.results[i] = content


def gather_uris(
    documents: t.List[t.Dict], gather_ids: bool = True
) -> t.Tuple[t.List[str], t.List[str], t.List[int]]:
    """
    Get the URLS out of all documents as denoted by ``{"_content": ...}``

    :param documents: list of dictionaries
    """
    uris = []
    mongo_keys = []
    ids = []
    for i, r in enumerate(documents):
        sub_uris, sub_mongo_keys = _gather_uris_for_document(r)
        if gather_ids:
            ids.extend([r['_id'] for _ in sub_uris])
        else:
            ids.append(i)
        uris.extend(sub_uris)
        mongo_keys.extend(sub_mongo_keys)
    return uris, mongo_keys, ids


def _gather_uris_for_document(r: t.Dict) -> t.Tuple[t.List[str], t.List[str]]:
    '''
    >>> _gather_uris_for_document({'a': {'_content': {'uri': 'test'}}})
    (['test'], ['a'])
    >>> d = {'b': {'a': {'_content': {'uri': 'test'}}}}
    >>> _gather_uris_for_document(d)
    (['test'], ['b.a'])
    >>> d = {'b': {'a': {'_content': {'uri': 'test', 'bytes': b'abc'}}}}
    >>> _gather_uris_for_document(d)
    ([], [])
    '''
    uris = []
    keys = []
    for k in r:
        if isinstance(r[k], dict) and '_content' in r[k]:
            if 'uri' in r[k]['_content'] and 'bytes' not in r[k]['_content']:
                keys.append(k)
                uris.append(r[k]['_content']['uri'])
        elif isinstance(r[k], dict) and '_content' not in r[k]:
            sub_uris, sub_keys = _gather_uris_for_document(r[k])
            uris.extend(sub_uris)
            keys.extend([f'{k}.{key}' for key in sub_keys])
    return uris, keys
