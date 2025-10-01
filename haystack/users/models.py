from typing import Any, ClassVar

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from haystack.core.models import UUIDMixin


class UserManager(BaseUserManager['User']):
    def _create_user_object(self, email: str, password: str, **extra_fields: Any) -> 'User':
        if email is None:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, email: str, password: str, **extra_fields: Any) -> 'User':
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields: Any) -> 'User':
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> 'User':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, UUIDMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = ''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()  # type: ignore[assignment]

    def __str__(self) -> str:
        return self.email
