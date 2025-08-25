from users.apps import UsersConfig
from django.urls import path
from users.views import PaymentViewSet
from rest_framework.routers import SimpleRouter


app_name = UsersConfig.name

router = SimpleRouter()
router.register("payment", PaymentViewSet)

urlpatterns = [

]
urlpatterns += router.urls
