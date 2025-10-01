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
    name = models.CharField(max_length=255, unique=True)
    geo_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Job(UUIDModel):
    company = models.ForeignKey(Company, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    location = models.ForeignKey(Location, related_name='jobs', on_delete=models.SET_NULL, null=True, blank=True)
    date_posted = models.DateField()

    date_found = models.DateField()
    populated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
