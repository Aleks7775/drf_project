from django.utils import timezone
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail

from config import settings
from users.models import User


@shared_task
def send_information(email):
    """Асинхронная рассылка писем пользователям об обновлении материалов курса"""
    send_mail('Обновление материала', 'Вышло новое обновление', settings.EMAIL_HOST_USER, [email])

@shared_task
def time_block_user():
    """Проверка и блокировка неактивных пользователей"""
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()
