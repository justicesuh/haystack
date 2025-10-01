from django.contrib import admin

from haystack.core.admin import UUIDModelAdmin
from haystack.users.models import User

admin.site.register(User, UUIDModelAdmin)
