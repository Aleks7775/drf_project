from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from online_training.models import Course, Lesson
from online_training.paginators import CustomPagination
from online_training.serliazers import CourseSerializer, LessonSerializer
from users.models import Followers
from users.permissions import IsModer, IsOwner
from online_training.tasks import send_information
from rest_framework.generics import get_object_or_404


class CourseViewSet(viewsets.ModelViewSet):
    """ Viewset for course"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Присваивания курса к пользователю"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """Проверка на модератора и пользователя"""
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, ~IsModer,) # инверсия (пользователь должен быть не модератор)
        elif self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsOwner,)
        return super().get_permissions()

    def get_queryset(self):
        """Проверяем, есть ли у пользователя права модератора, если пользователь не модератор, показываем только его курсы"""
        is_moderator = IsModer()
        if is_moderator.has_permission(self.request, self):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        """Функция для проверки и отправки рассылки пользователям которые подписаны на курс"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        subs_item = Followers.objects.filter(courses=instance)

        for follower in subs_item:
            send_information.delay(follower.user.email)

        return Response(serializer.data)


class LessonCreateAPIView(generics.CreateAPIView):
    """ Lesson create endpoint """
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated) # нет прав у не авторизованного пользователя, не модератор

    def perform_create(self, serializer):
        """Присваивания урока к пользователю"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """ Lesson list endpoint """
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    # queryset = Lesson.objects.all()

    def get_queryset(self):
        """Проверяем, есть ли у пользователя права модератора, если пользователь не модератор, показываем только его уроки"""
        is_moderator = IsModer()
        if is_moderator.has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Lesson create endpoint """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)  # либо модератор либо владелец


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Lesson update endpoint """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Lesson delete endpoint """
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)  # авторизован и владелец
