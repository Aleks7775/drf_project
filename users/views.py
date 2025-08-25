
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from users.models import Payment
from users.serliazers import PaymentSerializer
from rest_framework import filters


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    """Настройка фильтрации"""
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['pay_method', 'paid_lesson', 'paid_course']
    ordering_fields = ['pay_date']
