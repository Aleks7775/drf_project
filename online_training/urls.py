from django.urls import path
from online_training.apps import OnlineTrainingConfig
from rest_framework.routers import DefaultRouter

from online_training.views import (CourseViewSet, LessonCreateAPIView, LessonListAPIView,
                                   LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIViewAPIView)

app_name = OnlineTrainingConfig.name


router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIViewAPIView.as_view(), name='lesson-delete')
] + router.urls
