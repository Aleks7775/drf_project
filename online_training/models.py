from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, help_text="Название курса")
    picture = models.ImageField(
        upload_to="online_training/course/avatars",
        verbose_name="Аватар",
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name='Владелец')

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100, help_text="Название урока")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    picture = models.ImageField(
        upload_to="online_training/lesson/avatars",
        verbose_name="Аватар",
        blank=True,
        null=True,
    )
    video_url = models.URLField(max_length=200, verbose_name="Ссылка на видео", blank=True, null=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,  verbose_name="Курс"
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
