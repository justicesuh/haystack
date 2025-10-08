from django.contrib import admin

from haystack.core.admin import UUIDModelAdmin
from haystack.jobs.models import Company, Job, Location

admin.site.register(Company, UUIDModelAdmin)
admin.site.register(Location, UUIDModelAdmin)
admin.site.register(Job, UUIDModelAdmin)
