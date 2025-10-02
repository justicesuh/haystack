from django.contrib import admin

from haystack.core.admin import UUIDModelAdmin
from haystack.search.models import Search


class SearchAdmin(UUIDModelAdmin):
    list_display = ('__str__', 'location')
    search_fields = ('keywords',)


admin.site.register(Search, SearchAdmin)
