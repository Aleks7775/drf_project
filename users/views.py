from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (CreateAPIView, ListAPIView, UpdateAPIView,
                                     DestroyAPIView, get_object_or_404)
from rest_framework import status
from rest_framework.response import Response
from users.models import Payment, User, Followers
from online_training.models import Course
from users.permissions import IsOwner
from users.serliazers import PaymentSerializer, UserSerializer, FollowSerializer
from rest_framework import filters


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    """Настройка фильтрации"""
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['pay_method', 'paid_lesson', 'paid_course']
    ordering_fields = ['pay_date']


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Позволяет контролеру открыть доступ всем пользователям

    def perform_create(self, serializer):
        """Сохраняем нового пользователя при регистрации, активируем и кэшируем пароль"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class FollowersView(APIView):
    queryset = Followers.objects.all()
    serializer_class = FollowSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Followers.objects.filter(user=user, courses=course_item)
             # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
            status_code = status.HTTP_200_OK
            # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Followers.objects.create(user=user, courses=course_item)
            message = "подписка добавлена"
            status_code = status.HTTP_201_CREATED

        # Возвращаем ответ в API
        return Response({"message": message}, status=status_code)
