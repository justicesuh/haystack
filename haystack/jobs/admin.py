from django.contrib import admin

from haystack.core.admin import UUIDModelAdmin
from haystack.jobs.models import Company, Job, Location


class LocationAdmin(UUIDModelAdmin):
    list_display = ('name', 'geo_id')
    search_fields = ('name',)


admin.site.register(Company, UUIDModelAdmin)
admin.site.register(Job, UUIDModelAdmin)
admin.site.register(Location, LocationAdmin)
