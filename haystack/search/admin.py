from django.contrib import admin

from haystack.core.admin import UUIDModelAdmin
from haystack.search.models import Search, SearchSource, Source

admin.site.register(Search, UUIDModelAdmin)
admin.site.register(SearchSource, UUIDModelAdmin)
admin.site.register(Source, UUIDModelAdmin)
