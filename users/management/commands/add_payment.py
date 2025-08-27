from django.core.management.base import BaseCommand
from users.models import Payment, User, Course, Lesson
from datetime import datetime



class Command(BaseCommand):
    help = 'Add test payments to the database'

    def handle(self, *args, **kwargs):
        """Кастомная команда для записи данных в таблицу"""

        user = User.objects.first()  # Получим первого пользователя в базе
        course = Course.objects.first()  # Получим первый курс в базе
        lesson = Lesson.objects.first()  # Получим первый урок в базе

        payments = [
            {
                'user': user,
                'pay_date': datetime.now(),
                'paid_course': course,
                # 'paid_lesson': lesson,
                'pay_amount': 10000,
                'pay_method': 'Transfer',
            },
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added payment for {payment.user}'))
            else:
                self.stdout.write(self.style.WARNING(f'Payment already exists for {payment.user}'))