from django.contrib import admin
from django.http.request import HttpRequest

from haystack.core.typing import _FieldGroups, _ListOrTuple, _ModelT


class ModelAdmin(admin.ModelAdmin):
    """ModelAdmin with additional `created_at` and `updated_at` fields."""

    def get_readonly_fields(self, request: HttpRequest, obj: _ModelT | None = None) -> _ListOrTuple[str]:
        """Append `created_at` and `updated_at` fields if exist on model."""
        fields = tuple(super().get_readonly_fields(request, obj))
        return fields + tuple([field for field in ['created_at', 'updated_at'] if hasattr(self.model, field)])


class UUIDModelAdmin(ModelAdmin):
    """ModelAdmin with UUID field."""

    readonly_fields = ('uuid',)

    def get_fields(self, request: HttpRequest, obj: _ModelT | None = None) -> _FieldGroups:
        """Move UUID to beginning of field list."""
        fields = list(super().get_fields(request, obj))
        fields.remove('uuid')
        fields.insert(0, 'uuid')
        return fields
