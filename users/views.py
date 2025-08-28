
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView

from users.models import Payment, User
from users.serliazers import PaymentSerializer, UserSerializer
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
