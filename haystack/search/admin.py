from django.contrib import admin

from haystack.core.admin import UUIDModelAdmin
from haystack.search.models import Search

admin.site.register(Search, UUIDModelAdmin)
