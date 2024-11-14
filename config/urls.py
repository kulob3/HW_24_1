from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("course.urls", namespace="course")),
    path("", include("users.urls", namespace="users")),
]
