from rest_framework import viewsets
from rest_framework import permissions

from .models import Currency, Order, Trade, UserBalance
from .serializers import CurrencySerializer, OrderSerializer, TradeSerializer, UserBalanceSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    # permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated]


class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserBalanceViewSet(viewsets.ModelViewSet):
    queryset = UserBalance.objects.all()
    serializer_class = UserBalanceSerializer
    # permission_classes = [permissions.IsAuthenticated]
