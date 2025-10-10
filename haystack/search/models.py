from django.db import models
from django.utils.translation import gettext_lazy as _

from haystack.core.models import UUIDModel
from haystack.jobs.models import Location


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
    def geo_id(self) -> int:
        """Return Location `geo_id`."""
        geo_id = getattr(self.location, 'geo_id', None)
        if geo_id is None:
            return Location.WORLDWIDE
        return int(geo_id)

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

    def __str__(self) -> str:
        """Return Search and Source."""
        return f'{self.search} - {self.source}'
