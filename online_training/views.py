from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from online_training.models import Course, Lesson
from online_training.serliazers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated) # нет прав у не авторизованного пользователя, не модератор

    def perform_create(self, serializer):
        """Присваивания урока к пользователю"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    # queryset = Lesson.objects.all()

    def get_queryset(self):
        """Проверяем, есть ли у пользователя права модератора, если пользователь не модератор, показываем только его уроки"""
        is_moderator = IsModer()
        if is_moderator.has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)  # либо модератор либо владелец


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)  # авторизован и владелец
