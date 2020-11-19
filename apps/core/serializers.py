from rest_framework import serializers

from .models import Currency, Order, Trade, UserBalance


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name', 'verbose_name', 'acronym', 'currency_type']


# class User(AbstractUser):
#     pass


class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = ['user', 'currency', 'balance']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'origin_currency', 'destination_currency', 'order_type', 'price']


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['buyer_order', 'seller_order']
