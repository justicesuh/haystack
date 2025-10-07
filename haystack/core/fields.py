import uuid
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import Promise


class AutoCreatedField(models.DateTimeField):
    """A DateTimeField that populates on object creation."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault('auto_now_add', True)
        super().__init__(*args, **kwargs)


class AutoUpdatedField(models.DateTimeField):
    """A DateTimeField that updates on object save."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault('auto_now', True)
        super().__init__(*args, **kwargs)


class UUIDField(models.UUIDField):
    """A UUIDField with default arguments."""

    def __init__(
        self,
        verbose_name: str | Promise | None = None,
        primary_key: bool = False,
        version: int = 4,
        editable: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if version == 2:
            raise ValidationError('UUID version 2 is not supported.')

        if version < 1 or version > 5:
            raise ValidationError('UUID version is not valid.')

        default = getattr(uuid, f'uuid{version}')

        kwargs.setdefault('verbose_name', verbose_name)
        kwargs.setdefault('primary_key', primary_key)
        kwargs.setdefault('default', default)
        kwargs.setdefault('editable', editable)
        super().__init__(*args, **kwargs)
