from django.db import models


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
    video = models.FileField(
        upload_to="lessons/videos/", verbose_name="video", blank=True, null=True
    )
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, related_name="lessons", verbose_name="course",
        blank=True, null=True
    )

    class Meta:
        verbose_name = "lesson"
        verbose_name_plural = "lessons"

    def __str__(self):
        return self.name
