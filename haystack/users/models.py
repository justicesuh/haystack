from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from haystack.core.models import UUIDMixin


class User(AbstractUser, UUIDMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = ''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
