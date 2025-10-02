from django.db import models
from django.utils import timezone

from haystack.core.models import UUIDModel
from haystack.jobs.models import Job, Location


class Search(UUIDModel):
    keywords = models.CharField(max_length=255)
    location = models.ForeignKey(Location, related_name='searches', on_delete=models.SET_NULL, null=True, blank=True)

    easy_apply = models.BooleanField(default=False)
    flexibility = models.CharField(max_length=6, choices=Job.FLEXIBILITY_CHOICES, default=Job.ONSITE)

    last_executed = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('keywords', 'location', 'easy_apply', 'flexibility'),)
        verbose_name = 'search'
        verbose_name_plural = 'searches'

    @property
    def geo_id(self) -> int:
        if self.location is not None and self.location.geo_id is not None:
            return self.location.geo_id
        return Location.WORLDWIDE

    def update_last_executed(self) -> None:
        self.last_executed = timezone.now()
        self.save()

    def __str__(self) -> str:
        easy_apply = 'Yes' if self.easy_apply else 'No'
        flexibility = dict(Job.FLEXIBILITY_CHOICES)[self.flexibility]
        return f'{self.keywords} | Easy Apply: {easy_apply} | {flexibility}'
