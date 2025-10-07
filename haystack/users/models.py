from typing import Any, ClassVar, cast

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from haystack.core.models import UUIDMixin


class UserManager(BaseUserManager['User']):
    """Manager to create new users."""

    def create_user(self, email: str, password: str, **extra_fields: Any) -> 'User':
        """Create new user."""
        if email is None:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> 'User':
        """Create new super user."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, UUIDMixin):
    """Represent User using email address."""

    email = models.EmailField(_('email address'), unique=True)
    username = ''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects: ClassVar[DjangoUserManager['User']] = cast('DjangoUserManager[User]', UserManager())

    def __str__(self) -> str:
        """Return User email."""
        return self.email
