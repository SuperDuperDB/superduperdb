from .data_backend import MongoDBDataBackend as DataBackend
from .database_listener import MongoDBDatabaseListener as DatabaseListener
from .vector_search import MongoAtlasVectorSearcher as VectorSearcher
from importlib.metadata import version as _version, PackageNotFoundError

try:
    __version__ = _version("superduper_mongodb")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "DataBackend",
    "VectorSearcher",
    "DatabaseListener",
]
