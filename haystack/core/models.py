from django.db import models
from django.utils.translation import gettext_lazy as _

from haystack.core.fields import AutoCreatedField, AutoUpdatedField, UUIDField


class TimestampedMixin(models.Model):
    """Abstract base model that provides updating `created_at` and `updated_at` fields."""

    created_at = AutoCreatedField()
    updated_at = AutoUpdatedField()

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Abstract base model that provides uuid field."""

    uuid = UUIDField(_('UUID'))

    class Meta:
        abstract = True


class UUIDModel(TimestampedMixin, UUIDMixin):
    """Abstract base model that combines `TimeStampedMixin` and `UUIDMixin`."""

    class Meta:
        abstract = True
