from typing import TypeAlias, TypeVar

from django.contrib import admin

_K = TypeVar('_K')
_ListOrTuple: TypeAlias = list[_K] | tuple[_K, ...] | tuple[()]
_FieldGroups: TypeAlias = _ListOrTuple[str | _ListOrTuple[str]]


class ModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None) -> _ListOrTuple[str]:
        fields = super().get_readonly_fields(request, obj)
        return tuple(fields) + tuple([field for field in ['created_at', 'updated_at'] if hasattr(self.model, field)])


class UUIDModelAdmin(ModelAdmin):
    readonly_fields = ('uuid',)

    def get_fields(self, request, obj=None) -> _FieldGroups:
        fields = list(super().get_fields(request, obj))
        fields.remove('uuid')
        fields.insert(0, 'uuid')
        return fields
