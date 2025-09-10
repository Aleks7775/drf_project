from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from django.db.models import Count

from online_training.models import Course, Lesson
from online_training.validators import validate_words
from users.models import Followers


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(required=False, validators=[validate_words])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_course_lesson = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_course_lesson(self, obj):
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        """Метод для вывода is_subscribed Подписан или нет"""
        user = self.context['request'].user
        if Followers.objects.filter(user=user, courses=obj).exists():
            return "Подписан"
        else:
            return "Не подписан"
