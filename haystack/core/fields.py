from typing import Any

from django.db import models


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
