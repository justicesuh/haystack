from enum import IntEnum
from typing import Any, ClassVar

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from haystack.core.models import UUIDModel
from haystack.jobs.models import Job, Location


class Period(IntEnum):
    """Represent common search periods."""

    MONTH = 2592000
    WEEK = 604800
    DAY = 86400
    HOUR = 3600


class Status(models.TextChoices):
    """Enum representing `SearchSource` statuses."""

    IDLE = 'idle', _('Idle')
    SCHEDULED = 'scheduled', _('Scheduled')
    RUNNING = 'running', _('Running')
    SUCCESS = 'success', _('Success')
    ERROR = 'error', _('Error')


class Source(UUIDModel):
    """Model to represent Search sources."""

    name = models.CharField(max_length=32, unique=True)
    parser = models.CharField(max_length=32, unique=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Attach all `Search` objects to new `Source`."""
        is_create = self.pk is None
        super().save(*args, **kwargs)

        if is_create:

            def _attach_all_searches() -> None:
                search_ids = list(Search.objects.values_list('id', flat=True))
                if search_ids is None:
                    return
                SearchSource.objects.bulk_create(
                    (SearchSource(search_id=sid, source_id=self.id) for sid in search_ids),
                    ignore_conflicts=True,
                )

            transaction.on_commit(_attach_all_searches)

    def __str__(self) -> str:
        """Return Source name."""
        return self.name


class Search(UUIDModel):
    """Job Search representation."""

    keywords = models.CharField(max_length=255)
    location = models.ForeignKey(Location, related_name='searches', on_delete=models.SET_NULL, null=True, blank=True)

    easy_apply = models.BooleanField(default=False)
    is_hybrid = models.BooleanField(default=False)
    is_onsite = models.BooleanField(default=True)
    is_remote = models.BooleanField(default=False)

    sources = models.ManyToManyField(Source, through='search.SearchSource', related_name='searches')

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'search'
        verbose_name_plural = 'searches'

    @property
    def flexibility(self) -> str | None:
        """Compute Job flexibility based on Search booleans.

        Return None if multiple booleans are true.
        """
        if sum((self.is_hybrid, self.is_onsite, self.is_remote)) != 1:
            return None
        if self.is_hybrid:
            return Job.HYBRID
        if self.is_onsite:
            return Job.ONSITE
        if self.is_remote:
            return Job.REJECTED
        return None

    @property
    def geo_id(self) -> int:
        """Return Location `geo_id`."""
        geo_id = getattr(self.location, 'geo_id', None)
        if geo_id is None:
            return Location.WORLDWIDE
        return int(geo_id)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Attach all `Source` objects to new `Search`."""
        is_create = self.pk is None
        super().save(*args, **kwargs)

        if is_create:

            def _attach_all_sources() -> None:
                source_ids = list(Source.objects.values_list('id', flat=True))
                if not source_ids:
                    return
                SearchSource.objects.bulk_create(
                    (SearchSource(search_id=self.id, source_id=sid) for sid in source_ids),
                    ignore_conflicts=True,
                )

            transaction.on_commit(_attach_all_sources)

    def __str__(self) -> str:
        """Return string representation of Search."""
        easy_apply = 'Yes' if self.easy_apply else 'No'
        flexibility = ', '.join(
            [
                field.rsplit('_', 1)[-1].capitalize()
                for field in ['is_hybrid', 'is_onsite', 'is_remote']
                if getattr(self, field) is True
            ]
        )
        return f'{self.keywords} | Easy Apply: {easy_apply} | {flexibility}'


class SearchSource(UUIDModel):
    """ManyToMany through model between `Search` and `Source`."""

    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    last_executed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.IDLE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together: ClassVar[list[tuple[str, ...]]] = [('search', 'source')]

    def calculate_period(self, tolerance: float = 0.04) -> int:
        """Calculate search period in seconds based on `last_executed_at`.

        Args:
            tolerance (float): A tolerance factor for comparing time deltas.
            The default value of 0.04 is approximately equal to 1 / 24.

        """
        if not self.last_executed_at:
            return Period.MONTH

        delta = (timezone.now() - self.last_executed_at).total_seconds()
        for period in (Period.HOUR, Period.DAY, Period.WEEK):
            if delta <= period * (1 + tolerance):
                return period

        return Period.MONTH

    def set_status(self, status: Status) -> None:
        """Set status and save."""
        self.status = status
        if self.status in (Status.SUCCESS, Status.ERROR):
            self.last_executed_at = timezone.now()
        self.save()

    def __str__(self) -> str:
        """Return Search and Source."""
        return f'{self.search} - {self.source}'
