from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from django.urls import path
from users.views import (PaymentViewSet, UserCreateAPIView, UserListAPIView,
                         UserUpdateAPIView, UserDestroyAPIViewAPIView)
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


app_name = UsersConfig.name

router = SimpleRouter()
router.register("payment", PaymentViewSet)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('user/', UserListAPIView.as_view(), name='user-list'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', UserDestroyAPIViewAPIView.as_view(), name='user-delete')
]
urlpatterns += router.urls
