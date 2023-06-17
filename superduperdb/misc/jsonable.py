from pydantic import BaseModel, Field
import sys
import typing as t

__all__ = 'Factory', 'JSONable'

TYPE_ID_ATTR = 'type_id'
_NONE = object()


def Factory(factory: t.Callable, **ka) -> t.Any:
    return Field(default_factory=factory, **ka)


class JSONable(BaseModel):
    """
    JSONable is the base class for all superduperdb classes that can be
    converted to and from JSON
    """

    class Config:
        extra = 'forbid'  # Fail in deserializion if there are extra fields

    SUBCLASSES: t.ClassVar[t.Set[t.Type]] = set()
    TYPE_ID_TO_CLASS: t.ClassVar[t.Dict[str, t.Type]] = {}

    def deepcopy(self) -> 'JSONable':
        return self.copy(deep=True)

    def __init_subclass__(cls, *a, **ka):
        super().__init_subclass__(*a, **ka)
        cls.SUBCLASSES.add(cls)

        try:
            type_id = getattr(cls, TYPE_ID_ATTR)
        except AttributeError:
            return

        if not isinstance(type_id, str):
            (type_id,) = type_id.__args__

        if old_model := cls.TYPE_ID_TO_CLASS.get(type_id):
            print(f'Duplicate type_id: old={old_model}, new={cls}', file=sys.stderr)

        cls.TYPE_ID_TO_CLASS[type_id] = cls
