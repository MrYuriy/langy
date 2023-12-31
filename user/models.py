from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models
from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, related_name="user_set", blank=True, verbose_name=_("groups"))
    user_permissions = models.ManyToManyField(Permission, related_name="user_set", blank=True,
                                              verbose_name=_("user permissions"))

    def __str__(self):
        return self.email
