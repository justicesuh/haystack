from django.db import models
from django.utils import timezone

from haystack.core.models import UUIDModel


class Company(UUIDModel):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self) -> str:
        return self.name


class Location(UUIDModel):
    WORLDWIDE = 92000000

    name = models.CharField(max_length=255, unique=True)
    geo_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Job(UUIDModel):
    HYBRID = 'hybrid'
    ONSITE = 'onsite'
    REMOTE = 'remote'

    NEW = 'new'
    DISMISSED = 'dismissed'
    SAVED = 'saved'
    APPLIED = 'applied'
    REJECTED = 'rejected'
    INTERVIEWING = 'interviewing'
    OFFER = 'offer'
    ACCEPTED = 'accepted'
    WITHDRAWN = 'withdrawn'

    FLEXIBILITY_CHOICES = (
        (HYBRID, HYBRID.capitalize()),
        (ONSITE, ONSITE.capitalize()),
        (REMOTE, REMOTE.capitalize()),
    )

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
    date_posted = models.DateTimeField()

    search = models.ForeignKey('search.Search', related_name='jobs', on_delete=models.SET_NULL, null=True, blank=True)
    date_found = models.DateTimeField()
    populated = models.BooleanField(default=False)

    easy_apply = models.BooleanField(default=False)
    flexibility = models.CharField(max_length=6, choices=FLEXIBILITY_CHOICES, default=ONSITE)
    description = models.TextField(default='')
    raw_html = models.TextField(default='')

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=NEW)
    date_applied = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cached_status = self.status

    def update_status(self, new_status: str) -> None:
        if self.cached_status == new_status:
            return
        self.status = new_status
        event = Event.objects.create(
            event_type=Event.STATUS, job=self, old_status=self.cached_status, new_status=self.status
        )
        event.save()
        self.cached_status = self.status

        if self.status == Job.APPLIED:
            self.date_applied = timezone.now().date()
        self.save()

    def add_note(self, note: str) -> None:
        event = Event.objects.create(event_type=Event.NOTE, job=self, note=note)
        event.save()
        self.save()

    def __str__(self) -> str:
        return self.title


class Event(UUIDModel):
    NOTE = 'note'
    STATUS = 'status'

    EVENT_TYPE_CHOICES = (
        (NOTE, NOTE.capitalize()),
        (STATUS, STATUS.capitalize()),
    )

    event_type = models.CharField(max_length=6, choices=EVENT_TYPE_CHOICES)
    job = models.ForeignKey(Job, related_name='events', on_delete=models.CASCADE)

    old_status = models.CharField(max_length=12, choices=Job.STATUS_CHOICES, default='')
    new_status = models.CharField(max_length=12, choices=Job.STATUS_CHOICES, default='')

    note = models.TextField(default='')

    def __str__(self) -> str:
        ret = f'{self.job.title} | '
        if self.event_type == Event.NOTE:
            ret += self.note
        else:
            ret += f'{self.old_status} -> {self.new_status}'
        return ret
