from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from django.urls import include, path

from . import views


router = routers.DefaultRouter()
router.register(r'currency', views.CurrencyViewSet)
router.register(r'currency_pair', views.CurrencyPairViewSet)
router.register(r'user_balance', views.UserBalanceViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'trade', views.TradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token-auth/', obtain_jwt_token)
]
