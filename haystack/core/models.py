from django.db import models

from haystack.core.fields import AutoCreatedField, AutoUpdatedField


class TimestampedMixin(models.Model):
    """Abstract base model that provides updating `created_at` and `updated_at` fields."""

    created_at = AutoCreatedField()
    updated_at = AutoUpdatedField()

    class Meta:
        abstract = True
