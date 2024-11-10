from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="email address", help_text="indicate your email"
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name="first name",
        help_text="indicate your first",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name="last name",
        help_text="indicate your last",
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=15,
        verbose_name="phone number",
        help_text="indicate your phone number",
        blank=True,
        null=True,
    )
    sity = models.CharField(
        max_length=30,
        verbose_name="sity",
        help_text="indicate your sity",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="avatar",
        help_text="indicate your avatar",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
