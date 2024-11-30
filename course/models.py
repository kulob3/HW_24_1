from django.db import models
from users.models import User
from django.conf import settings



class Course(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="name", help_text="indicate course name"
    )
    preview = models.ImageField(
        upload_to="courses/previews/", verbose_name="preview", blank=True, null=True
    )
    description = models.TextField(
        verbose_name="description",
        help_text="indicate course description",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Owner",
        blank=True,
        null=True,
        help_text="Owner of the course",
    )
    video = models.URLField(verbose_name="video", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="price", default=1000)

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    description = models.TextField(
        verbose_name="description",
        blank=True,
        null=True,
        help_text="indicate lesson description",
    )
    preview = models.ImageField(
        upload_to="lessons/previews/", verbose_name="preview", blank=True, null=True
    )
    video = models.URLField(verbose_name="video", blank=True, null=True)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, related_name="lessons", verbose_name="course",
        blank=True, null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Owner",
        blank=True,
        null=True,
        help_text="Owner of the lesson",
    )

    class Meta:
        verbose_name = "lesson"
        verbose_name_plural = "lessons"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'subscription'
        verbose_name_plural = 'subscriptions'

    def __str__(self):
        return f'{self.user} subscribed to {self.course}'

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    stripe_product_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)
    stripe_session_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(max_length=400, verbose_name="link", help_text="Optional. URL.", blank=True, null=True)
