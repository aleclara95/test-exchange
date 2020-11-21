from rest_framework import viewsets
from rest_framework import permissions

from .models import Currency, CurrencyPair, Order, Trade, UserBalance
from .serializers import (CurrencySerializer, CurrencyPairSerializer,  OrderSerializer,
                          TradeSerializer, UserBalanceSerializer)
from .querysets import UserBalanceQuerySet


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    # permission_classes = [permissions.IsAuthenticated]


class CurrencyPairViewSet(viewsets.ModelViewSet):
    queryset = CurrencyPair.objects.all()
    serializer_class = CurrencyPairSerializer
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

    def get_queryset(self):
        qs = super(UserBalanceViewSet, self).get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        return qs
