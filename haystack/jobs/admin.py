from django.contrib import admin

from haystack.core.admin import UUIDModelAdmin
from haystack.jobs.models import Company, Job, Location


class JobAdmin(UUIDModelAdmin):
    list_display = ('title', 'easy_apply', 'populated')
    list_filter = ('easy_apply', 'populated', 'status')

    show_facets = admin.ShowFacets.ALWAYS


admin.site.register(Company, UUIDModelAdmin)
admin.site.register(Location, UUIDModelAdmin)
admin.site.register(Job, JobAdmin)
