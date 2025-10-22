from .data_backend import SQLDatabackend as DataBackend
from .database_listener import SQLDatabaseListener as DatabaseListener
from importlib.metadata import version as _version, PackageNotFoundError

try:
    __version__ = _version("superduper_sql")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["DataBackend", "DatabaseListener"]
