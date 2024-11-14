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



class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="user",
        help_text="indicate user",
        related_name="payments",
    )
    date = models.DateTimeField(
        auto_now_add=True, verbose_name="date", help_text="indicate date"
    )
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        verbose_name="course",
        help_text="indicate course",
        related_name="payments",
        blank=True,
        null=True,
    )
    lesson = models.ForeignKey(
        "course.Lesson",
        on_delete=models.CASCADE,
        verbose_name="lesson",
        help_text="indicate lesson",
        related_name="payments",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="amount",
    )
    payment_method = models.CharField(
        max_length=15,
        verbose_name="payment method",
        help_text="indicate payment method",
        choices=(("cash", "cash"), ("transfer", "transfer")),
    )

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"
