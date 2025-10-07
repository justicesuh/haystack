from typing import TypeAlias, TypeVar

from django.db.models.base import Model
from django.utils.functional import Promise

_StrOrPromise: TypeAlias = str | Promise

_ModelT = TypeVar('_ModelT', bound=Model)

_K = TypeVar('_K')
_ListOrTuple: TypeAlias = list[_K] | tuple[_K, ...] | tuple[()]
_FieldGroups: TypeAlias = _ListOrTuple[str | _ListOrTuple[str]]
