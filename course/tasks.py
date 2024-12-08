from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model


@shared_task
def send_course_update_email(user_email, course_name):
    send_mail(
        'Course Update',
        f'The course "{course_name}" has been updated.',
        [EMAIL_HOST_USER],
        [user_email],
        fail_silently=False,
    )


User = get_user_model()

@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)