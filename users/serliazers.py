from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import Payment, User, Followers, Donation


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FollowSerializer(ModelSerializer):

    class Meta:
        model = Followers
        fields = '__all__'


class DonationSerializer(ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

