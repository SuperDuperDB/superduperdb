import datetime
import typing as t
import uuid


from superduperdb.core.tasks import method_job, callable_job


def job(f):
    def wrapper(
        *args,
        distributed=False,
        db: t.Optional[t.Any] = None,
        dependencies: t.List[Job] = (),  # type: ignore[assignment]
        **kwargs,
    ):
        j = FunctionJob(callable=f, args=args, kwargs=kwargs)  # type: ignore[arg-type]
        return j(db=db, distributed=distributed, dependencies=dependencies)

    return wrapper


class Job:
    def __init__(
        self,
        args: t.Optional[t.List] = None,
        kwargs: t.Optional[t.Dict] = None,
    ):
        self.args = args
        self.kwargs = kwargs
        self.identifier = str(uuid.uuid4())
        self.callable = None
        self.db = None
        self.future = None

    def watch(self):
        return self.db.metadata.watch_job(identifier=self.identifier)

    def run_locally(self, db):
        try:
            out = self.callable(*self.args, db=db, **self.kwargs)
            db.metadata.update_job(self.identifier, 'status', 'success')
        except Exception as e:
            db.metadata.update_job(self.identifier, 'status', 'failed')
            raise e
        return out

    def run_on_dask(self, client, dependencies=()):
        raise NotImplementedError

    def dict(self):
        return {
            'identifier': self.identifier,
            'time': datetime.datetime.now(),
            'status': 'pending',
            'args': self.args,
            'kwargs': self.kwargs,
            'stdout': [],
            'stderr': [],
        }

    def __call__(
        self, db: t.Optional[t.Any] = None, distributed=False, dependencies=()
    ):
        raise NotImplementedError


class FunctionJob(Job):
    def __init__(
        self,
        callable: t.Callable,
        args: t.Optional[t.List] = None,
        kwargs: t.Optional[t.Dict] = None,
    ):
        super().__init__(args=args, kwargs=kwargs)
        self.callable = callable  # type: ignore[assignment]

    def dict(self):
        d = super().dict()
        d['cls'] = 'FunctionJob'
        return d

    def run_on_dask(self, client, dependencies=()):
        from superduperdb.misc.configs import build_config

        CFG = build_config()
        self.future = client.submit(
            callable_job,
            cfg=CFG,
            function_to_call=self.callable,
            job_id=self.identifier,
            args=self.args,
            kwargs=self.kwargs,
            key=self.identifier,
            dependencies=dependencies,
        )
        return

    def __call__(
        self, db: t.Optional[t.Any] = None, distributed=False, dependencies=()
    ):
        if db is None:
            from superduperdb.datalayer.base.build import build_datalayer

            db = build_datalayer()
        db.metadata.create_job(self.dict())
        if not distributed:
            self.run_locally(db)
        else:
            self.run_on_dask(client=db.distributed_client, dependencies=dependencies)
        return self


class ComponentJob(Job):
    def __init__(
        self,
        component_identifier: str,
        variety: str,
        method_name: str,
        args: t.Optional[t.List] = None,
        kwargs: t.Optional[t.Dict] = None,
    ):
        super().__init__(args=args, kwargs=kwargs)

        self.component_identifier = component_identifier
        self.method_name = method_name
        self.variety = variety
        self._component = None

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, value):
        self._component = value
        self.callable = getattr(self._component, self.method_name)

    def run_on_dask(self, client, dependencies=()):
        from superduperdb.misc.configs import build_config

        CFG = build_config()
        self.future = client.submit(
            method_job,
            cfg=CFG,
            variety=self.variety,
            identifier=self.component_identifier,
            method_name=self.method_name,
            job_id=self.identifier,
            args=self.args,
            kwargs=self.kwargs,
            key=self.identifier,
            dependencies=dependencies,
        )

        return

    def __call__(
        self, db: t.Optional[t.Any] = None, distributed=False, dependencies=()
    ):
        if db is None:
            from superduperdb.datalayer.base.build import build_datalayer

            db = build_datalayer()
        db.metadata.create_job(self.dict())
        if self.component is None:
            self.component = db.load(self.variety, self.component_identifier)
        if not distributed:
            self.run_locally(db)
        else:
            self.run_on_dask(client=db.distributed_client, dependencies=dependencies)
        return self

    def dict(self):
        d = super().dict()
        d.update(
            {
                'method_name': self.method_name,
                'component_identifier': self.component_identifier,
                'variety': self.variety,
                'cls': 'ComponentJob',
            }
        )
        return d
