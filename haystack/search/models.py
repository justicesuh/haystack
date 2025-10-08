from django.db import models

from haystack.core.models import UUIDModel
from haystack.jobs.models import Location


class Search(UUIDModel):
    """Job Search representation."""

    keywords = models.CharField(max_length=255)
    location = models.ForeignKey(Location, related_name='searches', on_delete=models.SET_NULL, null=True, blank=True)

    easy_apply = models.BooleanField(default=False)
    is_hybrid = models.BooleanField(default=False)
    is_onsite = models.BooleanField(default=True)
    is_remote = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'search'
        verbose_name_plural = 'searches'

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
