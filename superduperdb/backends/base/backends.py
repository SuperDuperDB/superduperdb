from ibis.backends.base import BaseBackend
from pymongo import MongoClient

from superduperdb.backends.filesystem.artifacts import FileSystemArtifactStore
from superduperdb.backends.ibis.datastore import IbisDataBackend
from superduperdb.backends.mongodb.artifacts import MongoArtifactStore
from superduperdb.backends.mongodb.datastore import MongoDataBackend
from superduperdb.backends.mongodb.metadata import MongoMetaDataStore
from superduperdb.backends.sqlalchemy.metadata import SQLAlchemyMetadata
from superduperdb.vector_search.in_memory import InMemoryVectorSearcher
from superduperdb.vector_search.lance import LanceVectorSearcher

data_backends = {'mongodb': MongoDataBackend, 'ibis': IbisDataBackend}

artifact_stores = {'mongodb': MongoArtifactStore, 'filesystem': FileSystemArtifactStore}

metadata_stores = {'mongodb': MongoMetaDataStore, 'sqlalchemy': SQLAlchemyMetadata}

vector_searcher_implementations = {
    'lance': LanceVectorSearcher,
    'in_memory': InMemoryVectorSearcher,
}

CONNECTIONS = {
    'pymongo': MongoClient,
    'ibis': BaseBackend,
}
