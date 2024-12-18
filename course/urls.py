from django.urls import path
from rest_framework.routers import SimpleRouter
from course.apps import CourseConfig
from course.views import (CourseViewSet, LessonCreateAPIView,
                          LessonDestroyAPIView, LessonListAPIView,
                          LessonRetrieveAPIView, LessonUpdateAPIView, SubscriptionAPIView, CreatePaymentView)

app_name = CourseConfig.name

router = SimpleRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
]
urlpatterns += router.urls