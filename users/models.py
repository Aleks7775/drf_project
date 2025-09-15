from django.contrib.auth.models import AbstractUser
from django.db import models

from online_training.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Аватар", blank=True, null=True
    )
    phone = models.CharField(
        max_length=30, verbose_name="Телефон", blank=True, null=True
    )
    city = models.CharField(
        blank=True, max_length=50, help_text="Введите страну проживания"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD = [
        ('Cash', 'Наличные'),
        ('Transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pay_date = models.DateTimeField(verbose_name='Дата оплаты', null=True, blank=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    pay_amount = models.IntegerField(verbose_name='сумма оплаты', null=True, blank=True)
    pay_method = models.CharField(max_length=20,choices=PAYMENT_METHOD, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Donation(models.Model):
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты", help_text="Укажите сумму платежа")
    session_id = models.CharField(max_length=255, verbose_name="Id сессии", null=True, blank=True)
    link = models.URLField(max_length=400, verbose_name="Ccылка на оплату", null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.amount
