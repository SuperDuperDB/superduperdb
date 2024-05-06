from collections import defaultdict
import dataclasses as dc
import uuid
import pandas

<<<<<<< HEAD
from superduperdb import logging
from superduperdb.backends.base.query import (
    CompoundSelect,
    Insert,
    Like,
    QueryComponent,
    QueryLinker,
    RawQuery,
    Select,
    TableOrCollection,
    _ReprMixin,
)
from superduperdb.backends.ibis.cursor import SuperDuperIbisResult
from superduperdb.backends.ibis.field_types import dtype
from superduperdb.base.document import Document
from superduperdb.base.exceptions import DatabackendException
from superduperdb.components.component import Component
from superduperdb.components.datatype import DataType
=======
import typing as t

from superduperdb.backends.base.query import Query, applies_to
from superduperdb.base.cursor import SuperDuperCursor
>>>>>>> 9d83d21ec (Deprecate Serializable)
from superduperdb.components.schema import Schema


def _model_update_impl_flatten(
    db,
    ids: t.List[t.Any],
    predict_id: str,
    outputs: t.Sequence[t.Any],
):
    table_records = []

    for ix in range(len(outputs)):
        for r in outputs[ix]:
            d = {
                '_input_id': str(ids[ix]),
                '_source': str(ids[ix]),
                'output': r,
            }
            table_records.append(d)

    for r in table_records:
        if isinstance(r['output'], dict) and '_content' in r['output']:
            r['output'] = r['output']['_content']['bytes']

    db.databackend.insert(f'_outputs.{predict_id}', table_records)


def _model_update_impl(
    db,
    ids: t.List[t.Any],
    predict_id: str,
    outputs: t.Sequence[t.Any],
    flatten: bool = False,
):
    if not outputs:
        return

    if flatten:
        return _model_update_impl_flatten(
            db, ids=ids, predict_id=predict_id, outputs=outputs
        )

    table_records = []
    for ix in range(len(outputs)):
        d = {
            '_input_id': str(ids[ix]),
            'output': outputs[ix],
        }
        table_records.append(d)

    for r in table_records:
        if isinstance(r['output'], dict) and '_content' in r['output']:
            r['output'] = r['output']['_content']['bytes']

    db.databackend.insert(f'_outputs.{predict_id}', table_records)


<<<<<<< HEAD
class IbisBackendError(DatabackendException):
    """
    This error represents ibis query related errors
    i.e when there is an error while executing an ibis query,
    use this exception to represent the error.
    """
=======
@dc.dataclass(kw_only=True, repr=False)
class IbisQuery(Query):
>>>>>>> 9d83d21ec (Deprecate Serializable)

    flavours: t.ClassVar[t.Dict[str, str]] = {
        'pre_like': '^.*\.like\(.*\)\.find',
        'post_like': '^.*\.([a-z]+)\(.*\)\.like(.*)$',
        'insert': '^[^\(]+\.insert\(.*\)$',
    }

    @property
    @applies_to('insert')
    def documents(self):
        return self.parts[0][1][0]

    @property
<<<<<<< HEAD
    def output_fields(self):
        return self.query_linker.output_fields

    def _get_query_component(
        self,
        name: str,
        type: str,
        args: t.Optional[t.Sequence] = None,
        kwargs: t.Optional[t.Dict] = None,
    ):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        return IbisQueryComponent(name, type=type, args=args, kwargs=kwargs)

    def outputs(self, *predict_ids):
        """
        This method returns a query which joins a query with the outputs
        for a table.

        :param key: The key on which the model was evaluated
        :param model: The model identifier for which to get the outputs
        :param version: The version of the model for which to get the outputs (optional)

        >>> q = t.filter(t.age > 25).outputs('txt', 'model_name')
        """
        assert self.query_linker is not None
        return IbisCompoundSelect(
            table_or_collection=self.table_or_collection,
            pre_like=self.pre_like,
            query_linker=self.query_linker._outputs(*predict_ids),
            post_like=self.post_like,
        )

    def compile(self, db: 'Datalayer', tables: t.Optional[t.Dict] = None):
        """
        Convert the current query to an ``ibis`` native query.

        :param db: The superduperdb connection
        :param tables: A dictionary of ``ibis`` tables to use for the query
        """
        assert self.pre_like is None, "pre_like must be None"
        assert self.post_like is None, "post_like must be None"
        assert self.query_linker is not None, "query_linker must be set"

        table_id = self.table_or_collection.identifier
        if tables is None:
            tables = {}
        if table_id not in tables:
            try:
                tables[table_id] = db.databackend.conn.table(table_id)
            except KeyError:
                tables[table_id] = db.databackend.in_memory_tables[table_id]

        return self.query_linker.compile(db, tables=tables)

    def get_all_tables(self):
        tables = [self.table_or_collection.identifier]
        if self.query_linker is not None:
            tables.extend(self.query_linker.get_all_tables())
        tables = list(set(tables))
        return tables

    def _get_all_fields(self, db):
        tables = self.get_all_tables()
        component_tables = []
        for tab in tables:
            component_tables.append(db.load('table', tab))
=======
    def tables(self):
        out = {self.identifier: self.db.tables[self.identifier]}
        for part in self.parts:
            for a in part[1]:
                if isinstance(a, IbisQuery):
                    out.update(a.tables)
            for v in part[2].values():
                if isinstance(v, IbisQuery):
                    out.update(v.tables)
        return out
>>>>>>> 9d83d21ec (Deprecate Serializable)

    @property
    def schema(self):
        fields = {}
        import pdb; pdb.set_trace()
        t = self.db.load('table', 'documents')
        tables = self.tables
        if len(tables) == 1:
            return self.db.tables[self.identifier].schema
        for t, c in self.tables.items():
            renamings = t.renamings
            tmp = c.schema.fields
            to_update = dict(
                (renamings[k], v) 
                if k in renamings else (k, v)
                for k, v in tmp.items() if k in renamings
            )
            fields.update(to_update)
        return Schema(f'_tmp:{self.identifier}', fields)

    @property
    def renamings(self):
        r = {}
        for part in self.parts:
            if part[0] == 'rename':
                r.update(part[1][0])
            if part[0] == 'relabel':
                r.update(part[1][0])
        return r

    def _execute_pre_like(self, parent):
        like_args = self.parts[0][1]
        like_kwargs = self.parts[0][2]
        vector_index = like_kwargs['vector_index']
        like = like_args[0] if like_args else like_kwargs['like']

        similar_ids, similar_scores = self.db.get_nearest(like, vector_index=vector_index)
        similar_scores = dict(zip(similar_ids, similar_scores))
        table = self.table_or_collection
        filter_query = eval(f'table.{self.primary_id}.isin(similar_ids)')
        new_query = self.table_or_collection.filter(filter_query)
    
        return IbisQuery(
            db=self.db,
            identifier=self.identifier,
            parts=[
                *new_query.parts,
                *self.parts[1:],
            ],
        )

    def _execute_post_like(self, parent):
        like_args = self.parts[-1][1]
        like_kwargs = self.parts[-1][2]
        vector_index = like_kwargs['vector_index']
        like = like_args[0] if like_args else like_kwargs['like']
        ids = [r[self.primary_id] for r in self.select_ids._execute(parent)]
        similar_ids, similar_scores = self.db.find_nearest(
            like,
            vector_index=vector_index,
            n=like_kwargs.get('n', 10),
        )
        similar_scores = dict(zip(similar_ids, similar_scores))
        output = self._execute(self[:-1].select_using_ids(similar_ids))
        output.scores = similar_scores
        return output

    def _execute_insert(self, parent):
        documents = self.documents
        for r in documents:
            if self.primary_id not in r:
                r[self.primary_id] = str(uuid.uuid4())
        ids = [r[self.primary_id] for r in documents]
        self._execute(parent, method='encode')
        return ids

    def _create_table_if_not_exists(self):
        tables = self.db.databackend.list_tables_or_collections()
        if self.identifier in tables:
            return
        self.db.databackend.create_table_and_schema(
            self.identifier,
            self.schema.raw,
        )

    def _execute(self, parent, method='encode'):
        output  = super()._execute(parent, method=method)
        assert isinstance(output, pandas.DataFrame)
        output = output.to_dict(orient='records')
        component_table = self.db.tables[self.table_or_collection]
        return SuperDuperCursor(
            raw_cursor=(r for r in output),
            db=self.db,
            id_field=component_table.primary_id,
            schema=component_table.schema,
        )

    @property
    def type(self):
        return defaultdict(lambda: 'select', {'insert': 'insert'})[self.flavour]
        
    @property
    def primary_id(self):
        return self.db.tables[self.identifier].primary_id

    def model_update(
        self,
        ids: t.List[t.Any],
        predict_id: str,
        outputs: t.Sequence[t.Any],
        flatten: bool = False,
        **kwargs,
    ):
        if not flatten:
            return _model_update_impl(
                db=self.db,
                ids=ids,
                predict_id=predict_id,
                outputs=outputs,
                flatten=flatten,
            )
        else:
            return _model_update_impl_flatten(
                db=self.db,
                ids=ids,
                predict_id=predict_id,
                outputs=outputs,
                flatten=flatten,
            )

    def add_fold(self, fold: str):
        return self.filter(self._fold == fold)

    def select_using_ids(self, ids: t.Sequence[str]):
        filter_query = eval(f'self.{self.primary_id}.isin(ids)')
        return self.filter(filter_query)

    @property
    def select_ids(self):
        return self.select(self.primary_id)

    @applies_to('select')
    def select_ids_of_missing_outputs(self, predict_id: str):
        output_table = self.db.tables[f'_outputs.{predict_id}']
        output_table = output_table.relabel({'_base': '_outputs.' + predict_id})
        out = self.anti_join(
            output_table,
            output_table._input_id == self[self.table_or_collection.primary_id],
        )
        return out

<<<<<<< HEAD
    def get_all_tables(self):
        out = []
        for member in self.members:
            out.extend(member.get_all_tables())
        return list(set(out))

    def _outputs(self, *identifiers):
        for identifier in identifiers:
            symbol_table = IbisQueryTable(
                identifier=f'_outputs.{identifier}',
                primary_id='output_id',
            )
            symbol_table = symbol_table.relabel(
                {'output': f'_outputs.{identifier}', '_fold': f'fold.{identifier}'}
            )
            attr = getattr(self, self.table_or_collection.primary_id)
            other_query = self.join(symbol_table, symbol_table._input_id == attr)
            return other_query

    def __call__(self, *args, **kwargs):
        primary_id = (
            [self.primary_id]
            if isinstance(self.primary_id, str)
            else self.primary_id[:]
        )

        def my_filter(item):
            return (
                [item.primary_id]
                if isinstance(item.primary_id, str)
                else item.primary_id
            )

        for a in args:
            if isinstance(a, IbisQueryLinker) or isinstance(a, IbisQueryTable):
                primary_id.extend(my_filter(a))

        for v in kwargs.values():
            if isinstance(v, IbisQueryLinker) or isinstance(v, IbisQueryTable):
                primary_id.extend(my_filter(v))

        from superduperdb.backends.ibis.data_backend import INPUT_KEY

        primary_id = [p for p in primary_id if p != INPUT_KEY]
        if self.members[-1].name in JOIN_MEMBERS:
            pid = args[0].primary_id
            if isinstance(pid, str):
                primary_id = [*primary_id, pid]
            else:
                primary_id = [*primary_id, *pid[:]]
        if self.members[-1].name == 'group_by':
            primary_id = [x for x in primary_id if x != args[0]]
        members = [*self.members[:-1], self.members[-1](*args, **kwargs)]
        primary_id = sorted(list(set(primary_id)))
        primary_id = primary_id[0] if len(primary_id) == 1 else primary_id
        return type(self)(
            table_or_collection=self.table_or_collection,
            members=members,
            primary_id=primary_id,
        )

    def compile(self, db: 'Datalayer', tables: t.Optional[t.Dict] = None):
        table_id = self.table_or_collection.identifier
        if tables is None:
            tables = {}
        if table_id not in tables:
            tables = {table_id: db.databackend.conn.table(table_id)}
        result = tables[table_id]
        for member in self.members:
            result, tables = member.compile(parent=result, db=db, tables=tables)
        return result, tables

    def execute(self, db):
        native_query, _ = self.compile(db)
        try:
            result = native_query.execute()
        except Exception as exc:
            raise IbisBackendError(
                f'{native_query} Wrong query or not supported yet :: {exc}'
            )
        for column in result.columns:
            result[column] = result[column].map(
                db.databackend.db_helper.recover_data_format
            )
        return result


class QueryType(str, enum.Enum):
    '''
    This class holds type of query
    query: This means Query and can be called
    attr: This means Attribute and cannot be called
    '''

    QUERY = 'query'
    ATTR = 'attr'


@dc.dataclass(repr=False, kw_only=True)
class Table(Component):
    """
    This is a representation of an SQL table in ibis,
    saving the important meta-data associated with the table
    in the ``superduperdb`` meta-data store.
    {component_params}:param schema: The schema of the table
    :param primary_id: The primary id of the table
    """

    type_id: t.ClassVar[str] = 'table'
    __doc__ = __doc__.format(component_params=Component.__doc__)

    schema: Schema
    primary_id: str = 'id'

    def __post_init__(self, artifacts):
        super().__post_init__(artifacts)
        if '_fold' not in self.schema.fields:
            self.schema = Schema(
                self.schema.identifier,
                fields={**self.schema.fields, '_fold': dtype('str')},
            )

        assert self.primary_id != '_input_id', '"_input_id" is a reserved value'

    def pre_create(self, db: 'Datalayer'):
        assert self.schema is not None, "Schema must be set"
        # TODO why? This is done already
        for e in self.schema.encoders:
            db.add(e)
        if db.databackend.in_memory:
            if '_outputs' in self.identifier:
                db.databackend.in_memory_tables[
                    self.identifier
                ] = db.databackend.create_table_and_schema(
                    self.identifier, self.schema.raw
                )

                return

        try:
            db.databackend.create_table_and_schema(self.identifier, self.schema.raw)
        except Exception as e:
            if 'already exists' in str(e):
                pass
            else:
                raise e

    @staticmethod
    def infer_schema(data: t.Mapping[str, t.Any], identifier: t.Optional[str] = None):
        """
        Infer a schema from a given data object

        :param data: The data object
        :param identifier: The identifier for the schema, if None, it will be generated
        :return: The inferred schema
        """
        from superduperdb.misc.auto_schema import infer_schema

        return infer_schema(data, identifier=identifier, ibis=True)

    @property
    def table_or_collection(self):
        return IbisQueryTable(self.identifier, primary_id=self.primary_id)

    def compile(self, db: 'Datalayer', tables: t.Optional[t.Dict] = None):
        return IbisQueryTable(self.identifier, primary_id=self.primary_id).compile(
            db, tables=tables
        )

    def insert(self, documents, **kwargs):
        return IbisQueryTable(
            identifier=self.identifier, primary_id=self.primary_id
        ).insert(documents, **kwargs)

    def like(self, r: 'Document', vector_index: str, n: int = 10):
        return IbisQueryTable(
            identifier=self.identifier, primary_id=self.primary_id
        ).like(r=r, vector_index=vector_index, n=n)

    def outputs(self, *predict_ids):
        return IbisQueryTable(
            identifier=self.identifier, primary_id=self.primary_id
        ).outputs(*predict_ids)

    def __getattr__(self, item):
        return getattr(
            IbisQueryTable(identifier=self.identifier, primary_id=self.primary_id), item
        )

    def __getitem__(self, item):
        return IbisQueryTable(
            identifier=self.identifier, primary_id=self.primary_id
        ).__getitem__(item)

    def to_query(self):
        return IbisCompoundSelect(
            table_or_collection=IbisQueryTable(
                self.identifier, primary_id=self.primary_id
            ),
            query_linker=IbisQueryLinker(
                table_or_collection=IbisQueryTable(
                    self.identifier, primary_id=self.primary_id
                )
            ),
        )


@dc.dataclass(repr=False)
class IbisQueryTable(_ReprMixin, TableOrCollection, Select):
    """
    This is a symbolic representation of a table
    for building ``IbisCompoundSelect`` queries.

    :param primary_id: The primary id of the table
    """

    primary_id: str = 'id'

    def compile(self, db: 'Datalayer', tables: t.Optional[t.Dict] = None):
        if tables is None:
            tables = {}
        if self.identifier not in tables:
            tables[self.identifier] = db.databackend.conn.table(self.identifier)
        return tables[self.identifier], tables

    def repr_(self):
        return self.identifier

    def add_fold(self, fold: str) -> Select:
        return self.filter(self.fold == fold)

    def outputs(self, *predict_ids):
        """
        This method returns a query which joins a query with the model outputs.

        :param model: The model identifier for which to get the outputs

        >>> q = t.filter(t.age > 25).outputs('model_name', db)

        The above query will return the outputs of the `model_name` model
        with t.filter() ids.
        """
        return IbisCompoundSelect(
            table_or_collection=self, query_linker=self._get_query_linker(members=[])
        ).outputs(*predict_ids)

    @property
    def id_field(self):
        return self.primary_id

    @property
    def select_table(self) -> Select:
        return self

    @property
    def select_ids(self) -> Select:
        return self.select(self.primary_id)

    def select_using_ids(self, ids: t.Sequence[t.Any]) -> Select:
        return self.filter(self[self.primary_id].isin(ids))

    def select_ids_of_missing_outputs(self, predict_id: str) -> Select:
        output_table = IbisQueryTable(
            identifier=f'_outputs.{predict_id}',
            primary_id='output_id',
        )
        return self.anti_join(
            output_table, output_table._input_id == self[self.primary_id]
        )

    def select_single_id(self, id):
        return self.filter(getattr(self, self.primary_id) == id)

    def __getitem__(self, item):
        return IbisCompoundSelect(
            table_or_collection=self,
            query_linker=self._get_query_linker(
                members=[IbisQueryComponent('__getitem__', type=QueryType.ATTR)],
            ),
        )(item)

    def _insert(self, documents, **kwargs):
        return IbisInsert(documents=documents, kwargs=kwargs, table_or_collection=self)

    def _get_query(
        self,
        pre_like: t.Optional[Like] = None,
        query_linker: t.Optional[QueryLinker] = None,
        post_like: t.Optional[Like] = None,
    ) -> IbisCompoundSelect:
        return IbisCompoundSelect(
            pre_like=pre_like,
            query_linker=query_linker,
            post_like=post_like,
            table_or_collection=self,
        )

    def _get_query_component(
        self,
        k,
    ):
        return IbisQueryComponent(name=k, type=QueryType.ATTR)

    def _get_query_linker(self, members) -> IbisQueryLinker:
        return IbisQueryLinker(
            table_or_collection=self, members=members, primary_id=self.primary_id
        )

    def insert(
        self,
        *args,
        **kwargs,
    ):
        return self._insert(*args, **kwargs)

    def _delete(self, *args, **kwargs):
        return super()._delete(*args, **kwargs)

    def execute(self, db):
        return db.databackend.conn.table(self.identifier).execute()

    def model_update(
        self,
        db,
        ids: t.List[t.Any],
        predict_id: str,
        outputs: t.Sequence[t.Any],
        flatten: bool = False,
        **kwargs,
    ):
        return _model_update_impl(
            db, ids=ids, predict_id=predict_id, outputs=outputs, flatten=flatten
        )


def _compile_item(item, db, tables):
    if hasattr(item, 'compile') and isinstance(
        getattr(item, 'compile'), types.MethodType
    ):
        return item.compile(db, tables=tables)
    if isinstance(item, list) or isinstance(item, tuple):
        compiled = []
        for x in item:
            c, tables = _compile_item(x, db, tables=tables)
            compiled.append(c)
        return compiled, tables
    elif isinstance(item, dict):
        c = {}
        for k, v in item.items():
            c[k], tables = _compile_item(v, db, tables=tables)
        return c, tables
    return item, tables


def _get_all_tables(item):
    if isinstance(item, (IbisQueryLinker, IbisCompoundSelect)):
        return item.get_all_tables()
    elif isinstance(item, IbisQueryTable):
        return [item.identifier]
    elif isinstance(item, list) or isinstance(item, tuple):
        return sum([_get_all_tables(x) for x in item], [])
    elif isinstance(item, dict):
        return sum([_get_all_tables(x) for x in item.values()], [])
    else:
        return []


@dc.dataclass
class IbisQueryComponent(QueryComponent):
    """
    This class represents a component of an ``ibis`` query.
    For example ``filter`` in ``t.filter(t.age > 25)``.
    """

    __doc__ = __doc__ + QueryComponent.__doc__  # type: ignore[operator]

    @property
    def primary_id(self):
        assert self.type == QueryType.QUERY, 'can\'t get primary id of an attribute'
        primary_id = []
        for a in self.args:
            if isinstance(a, IbisQueryComponent) and a.type == QueryType.QUERY:
                primary_id.extend(a.primary_id)
            if isinstance(a, IbisQueryTable):
                primary_id.append(a.primary_id)
            if isinstance(a, IbisCompoundSelect):
                primary_id.extend(a.primary_id)
        for a in self.kwargs.values():
            if isinstance(a, IbisQueryComponent) and a.type == QueryType.QUERY:
                primary_id.extend(a.primary_id)
            if isinstance(a, IbisQueryTable):
                primary_id.append(a.primary_id)
            if isinstance(a, IbisCompoundSelect):
                primary_id.extend(a.primary_id)
        return sorted(list(set(primary_id)))

    @property
    def renamings(self):
        if self.name == 'rename':
            return self.args[0]
        elif self.name == 'relabel':
            return self.args[0]
        else:
            out = {}
            if self.args is not None:
                for a in self.args:
                    if isinstance(
                        a, (IbisCompoundSelect, IbisQueryLinker, IbisQueryComponent)
                    ):
                        out.update(a.renamings)
            if self.kwargs is not None:
                for v in self.kwargs.values():
                    if isinstance(
                        v, (IbisCompoundSelect, IbisQueryLinker, IbisQueryComponent)
                    ):
                        out.update(v.renamings)
            return out

    def repr_(self) -> str:
        """
        >>> IbisQueryComponent('__eq__(2)', type=QueryType.QUERY, args=[1, 2]).repr_()
        """
        out = super().repr_()
        match = re.match('.*__([a-z]+)__\(([a-z0-9_\.\']+)\)', out)
        symbol = match.groups()[0] if match is not None else None

        if symbol == 'getitem':
            assert match is not None
            return f'[{match.groups()[1]}]'

        lookup = {'gt': '>', 'lt': '<', 'eq': '=='}
        if match is not None and match.groups()[0] in lookup:
            out = f' {lookup[match.groups()[0]]} {match.groups()[1]}'
        return out

    def compile(
        self, parent: t.Any, db: 'Datalayer', tables: t.Optional[t.Dict] = None
    ):
        if self.type == QueryType.ATTR:
            return getattr(parent, self.name), tables
        args, tables = _compile_item(self.args, db, tables=tables)
        kwargs, tables = _compile_item(self.kwargs, db, tables=tables)
        return getattr(parent, self.name)(*args, **kwargs), tables

    def get_all_tables(self):
        out = []
        out.extend(_get_all_tables(self.args))
        out.extend(_get_all_tables(self.kwargs))
        return list(set(out))


@dc.dataclass
class IbisInsert(Insert):
    def __post_init__(self):
        if isinstance(self.documents, pandas.DataFrame):
            self.documents = [
                Document(r) for r in self.documents.to_dict(orient='records')
            ]

    def _encode_documents(self, table: Table) -> t.List[t.Dict]:
        return [r.encode(table.schema) for r in self.documents]

    def execute(self, db):
        table = db.load(
            'table',
            self.table_or_collection.identifier,
        )
        encoded_documents = self._encode_documents(table=table)
        ids = [r[table.primary_id] for r in encoded_documents]

        db.databackend.insert(
            self.table_or_collection.identifier, raw_documents=encoded_documents
        )
        return ids
=======
    def select_single_id(self, id: str):
        table = self.table_or_collection
        filter_query = eval(f'table.{self.primary_id} == id')
        return self.filter(filter_query)
>>>>>>> 9d83d21ec (Deprecate Serializable)

    @property
    def select_table(self):
        return self.table_or_collection
