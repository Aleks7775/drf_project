from http.client import responses

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from online_training.models import Lesson, Course
from users.models import User, Followers


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="")
        self.course = Course.objects.create(title="Первый курс")
        self.lesson = Lesson.objects.create(title="Урок", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)


    def test_lesson_retrieve(self):
        """Тест на статус и просмотр урока"""
        url = reverse("online_training:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), "Урок"     #self.lesson.title
        )

    def test_lesson_create(self):
        """Тест на статус и добавления урока"""
        url = reverse("online_training:lesson-create")
        # self.course = Course.objects.create(title="Первый курс")
        data = {
            "title": "Программирование",
            "course": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """Тест на статус и обновление урока"""
        url = reverse("online_training:lesson-update", args=(self.lesson.pk,))
        data = {
            "title": "урок по программированию"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), "урок по программированию"
        )

    def test_lesson_delete(self):
        """Тест на статус и удаление урока"""
        url = reverse("online_training:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        """Тест на статус и просмотр всех уроков"""
        url = reverse("online_training:lesson-list")
        response = self.client.get(url)
        # print(response.json())
        data = response.json()
        result = {'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.lesson.pk,
                        'video_url': None,
                        'title': self.lesson.title,
                        'description': None,
                        'picture': None,
                        'course': self.course.pk,
                        'owner': self.user.pk}
                ]}
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_subscribe_course(self):
        """Тест работы подписки на обновления курса"""
        url = reverse("users:followers-view")
        data = {
            "id": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("message"), "подписка добавлена")
        response = self.client.post(url, data)
        self.assertEqual(response.data.get("message"), "подписка удалена")
