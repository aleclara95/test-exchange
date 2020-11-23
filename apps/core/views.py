from rest_framework import permissions, viewsets, views
from rest_framework.decorators import api_view

from .filters import OrderFilter, TradeFilter, UserBalanceFilter
from .models import Currency, CurrencyPair, Order, Trade, UserBalance
from .serializers import (CurrencySerializer, CurrencyPairSerializer,  OrderSerializer,
                          TradeSerializer, UserBalanceSerializer, UserSerializer,
                          UserSerializerWithToken)
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
    filter_class = OrderFilter


class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_class = TradeFilter


class UserBalanceViewSet(viewsets.ModelViewSet):
    queryset = UserBalance.objects.all()
    serializer_class = UserBalanceSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_class = UserBalanceFilter

    def get_queryset(self):
        qs = super(UserBalanceViewSet, self).get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        return qs


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(views.APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
