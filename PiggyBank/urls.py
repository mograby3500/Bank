from django.urls import path
from core.views import *
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router= routers.SimpleRouter()
router.register(r'categories', CategoryModelViewSet, basename= 'category')
router.register(r'transactions', TransactionModelViewSet, basename= 'transaction')

urlpatterns = [
    path("login/", obtain_auth_token, name= "obtain-auth-token"),
    path("currencies/", CurrencyListAPIView.as_view(), name= 'currencies'),
] + router.urls
