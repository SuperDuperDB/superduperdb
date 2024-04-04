"""
LLM model test cases.
All the llm model can use the check_xxx func to test the intergration with db.
"""

from superduperdb.backends.ibis.field_types import dtype
from superduperdb.backends.ibis.query import Schema, Table
from superduperdb.backends.mongodb.data_backend import MongoDataBackend
from superduperdb.backends.mongodb.query import Collection
from superduperdb.base.document import Document
from superduperdb.components.listener import Listener


def check_predict(db, llm):
    """Test whether db can call model prediction normally."""
    db.add(llm)
    result = llm.predict_one("1+1=")
    assert isinstance(result, str)


def check_llm_as_listener_model(db, llm):
    """Test whether the model can predict the data in the database normally"""
    collection_name = "question"
    datas = [
        Document({"question": f"1+{i}=", "id": str(i), '_fold': 'train'})
        for i in range(10)
    ]
    if isinstance(db.databackend, MongoDataBackend):
        db.execute(Collection(collection_name).insert_many(datas))
        select = Collection(collection_name).find()
    else:
        schema = Schema(
            identifier=collection_name,
            fields={
                "id": dtype("str"),
                "question": dtype("str"),
            },
        )
        table = Table(identifier=collection_name, schema=schema)
        db.add(table)
        db.execute(table.insert(datas))
        select = table.select("id", "question")

    db.add(
        Listener(
            select=select,
            key="question",
            model=llm,
        )
    )

    if isinstance(db.databackend, MongoDataBackend):
        output_select = Collection(collection_name).find()
    else:
        output_select = table.select("id", "question").outputs(
            f'question::{llm.identifier}::0::0'
        )

    results = db.execute(output_select)
    for result in results:
        output = result[f'_outputs.question::{llm.identifier}::0::0']
        assert isinstance(output, str)


# TODO: add test for llm_cdc
def check_llm_cdc(db, llm):
    """Test whether the model predicts normally for incremental data"""
    pass


# TODO: Expanded into a test tool class,
# Used to test whether all model objects are normally compatible with superduperdb
