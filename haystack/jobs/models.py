import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from django.db import models
from django.utils import dateparse, timezone

from haystack.core.models import UUIDModel

if TYPE_CHECKING:
    from haystack.search.models import SearchSource


logger = logging.getLogger(__name__)


class Company(UUIDModel):
    """Model representing LinkedIn company."""

    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self) -> str:
        """Return Company name."""
        return self.name


class Location(UUIDModel):
    """Model representing geographic location.

    Optional `geo_id` must conform to Bing Geo.
    """

    WORLDWIDE = 92000000

    name = models.CharField(max_length=255, unique=True)
    geo_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self) -> str:
        """Return Location name."""
        return self.name


class JobManager(models.Manager):
    """Custom model manager for Job."""

    def parse_datetime(self, datetime_str: str) -> datetime | None:
        """Parse datetime string and make timezone aware."""
        dt = dateparse.parse_datetime(datetime_str)
        if dt is None:
            logger.warning('dateparse.parse_datetime failed for %s. Setting to None', datetime_str)
            return None
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
        return dt

    def add_job(self, job: dict, search_source: 'SearchSource') -> bool:
        """Add parsed job to database."""
        company, _ = Company.objects.get_or_create(url=job['company_url'], defaults={'name': job['company']})

        location = None
        if job['location'] is not None:
            location, _ = Location.objects.get_or_create(name=job['location'])

        _, created = self.get_or_create(
            url=job['url'],
            defaults={
                'company': company,
                'title': job['title'],
                'location': location,
                'date_posted': self.parse_datetime(job['date_posted']),
                'search_source': search_source,
                'date_found': self.parse_datetime(job['date_found']),
            },
        )
        return created

    def add_jobs(self, jobs: list[dict], search_source: 'SearchSource') -> int:
        """Add parsed jobs to database."""
        return sum(1 for job in jobs if self.add_job(job, search_source))


class Job(UUIDModel):
    """Model representing Job application."""

    HYBRID = 'hybrid'
    ONSITE = 'onsite'
    REMOTE = 'remote'

    FLEXIBILITY_CHOICES = (
        (HYBRID, HYBRID.capitalize()),
        (ONSITE, ONSITE.capitalize()),
        (REMOTE, REMOTE.capitalize()),
    )

    NEW = 'new'
    EXPIRED = 'expired'
    DISMISSED = 'dismissed'
    SAVED = 'saved'
    APPLIED = 'applied'
    REJECTED = 'rejected'
    INTERVIEWING = 'interviewing'
    OFFER = 'offer'
    ACCEPTED = 'accepted'
    WITHDRAWN = 'withdrawn'

    STATUS_CHOICES = (
        (NEW, NEW.capitalize()),
        (DISMISSED, DISMISSED.capitalize()),
        (SAVED, SAVED.capitalize()),
        (APPLIED, APPLIED.capitalize()),
        (REJECTED, REJECTED.capitalize()),
        (INTERVIEWING, INTERVIEWING.capitalize()),
        (OFFER, OFFER.capitalize()),
        (ACCEPTED, ACCEPTED.capitalize()),
        (WITHDRAWN, WITHDRAWN.capitalize()),
    )

    company = models.ForeignKey(Company, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    location = models.ForeignKey(Location, related_name='jobs', on_delete=models.SET_NULL, null=True, blank=True)
    date_posted = models.DateTimeField(null=True, blank=True)

    search_source = models.ForeignKey(
        'search.SearchSource', related_name='jobs', on_delete=models.SET_NULL, null=True, blank=True
    )
    date_found = models.DateField(null=True, blank=True)
    populated = models.BooleanField(default=False)

    easy_apply = models.BooleanField(default=False)
    flexibility = models.CharField(max_length=6, choices=FLEXIBILITY_CHOICES, default=ONSITE)
    description = models.TextField(default='')
    raw_html = models.TextField(default='')

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=NEW)
    date_applied = models.DateTimeField(null=True, blank=True)

    objects = JobManager()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Cache Job status to track event history."""
        super().__init__(*args, **kwargs)
        self.cached_status = self.status

    def update_status(self, new_status: str) -> None:
        """Update Job status and create Event.

        Use instead of updating `status` directly.
        """
        if self.cached_status == new_status:
            return
        self.status = new_status
        event = Event.objects.create(
            event_type=Event.STATUS, job=self, old_status=self.cached_status, new_status=self.status
        )
        event.save()
        self.cached_status = self.status

        if self.status == Job.APPLIED:
            self.date_applied = timezone.now()
        self.save()

    def add_note(self, note: str) -> None:
        """Add note to Job."""
        event = Event.objects.create(event_type=Event.NOTE, job=self, note=note)
        event.save()
        self.save()

    def __str__(self) -> str:
        """Return Job title."""
        return self.title


class Event(UUIDModel):
    """Represents Job history event."""

    NOTE = 'note'
    STATUS = 'status'

    EVENT_TYPE_CHOICES = (
        (NOTE, NOTE.capitalize()),
        (STATUS, STATUS.capitalize()),
    )

    event_type = models.CharField(max_length=6, choices=EVENT_TYPE_CHOICES)
    job = models.ForeignKey(Job, related_name='events', on_delete=models.CASCADE)

    note = models.TextField(default='')

    old_status = models.CharField(max_length=12, choices=Job.STATUS_CHOICES, default='')
    new_status = models.CharField(max_length=12, choices=Job.STATUS_CHOICES, default='')

    def __str__(self) -> str:
        """Return string representation of Event."""
        ret = f'{self.job.title} | '
        if self.event_type == Event.NOTE:
            ret += self.note
        else:
            ret += f'{self.old_status} -> {self.new_status}'
        return ret
