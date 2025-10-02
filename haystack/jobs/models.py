from django.db import models

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

    def __str__(self) -> str:
        return self.title
