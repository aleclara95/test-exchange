from rest_framework import serializers

from .models import Currency, CurrencyPair, Order, Trade, UserBalance


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = []


class CurrencyPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyPair
        exclude = []


# class User(AbstractUser):
#     pass


class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        exclude = []


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['modified_date']


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        exclude = ['modified_date']
