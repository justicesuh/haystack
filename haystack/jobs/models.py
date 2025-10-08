from django.db import models

from haystack.core.models import UUIDModel


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

    name = models.CharField(max_length=255, unique=True)
    geo_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self) -> str:
        """Return Location name."""
        return self.name


class Job(UUIDModel):
    """Model representing Job application."""

    company = models.ForeignKey(Company, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    location = models.ForeignKey(Location, related_name='jobs', on_delete=models.SET_NULL, null=True, blank=True)
    date_posted = models.DateField()

    def __str__(self) -> str:
        """Return Job title."""
        return self.title
