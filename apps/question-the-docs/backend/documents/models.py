from pydantic.v1 import BaseModel, Field


class Repo(str):
    superduperdb = 'superduperdb'
    langchain = 'langchain'
    fastchat = 'fastchat'


class Query(BaseModel):
    query: str = Field(...)
    collection_name: Repo = Field(...)


class Answer(BaseModel):
    answer: str = Field(...)
    source_urls: list = Field(...)
