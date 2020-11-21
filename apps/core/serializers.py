from rest_framework import serializers

from django.conf import settings

from .models import Currency, CurrencyPair, Order, Trade, User, UserBalance


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
    currency_pair = serializers.CharField()

    class Meta:
        model = Order
        exclude = ['modified_date']
        read_only_fields = ['user', 'original_amount', 'mid_destinations']

    def create(self, validated_data):
        # Get currency pair
        currency_pair = validated_data.pop('currency_pair')
        currencies = currency_pair.split('/')
        if len(currencies) != 2:
            # The ideal here would be to use a custom exception
            raise Exception("Invalid currency pair format")
        origin_currency = currencies[0]
        destination_currency = currencies[1]
        currency_pair = CurrencyPair.objects.get(origin__acronym=origin_currency,
                                                 destination__acronym=destination_currency)

        validated_data['currency_pair'] = currency_pair

        # Get original amount
        validated_data['original_amount'] = validated_data['amount']

        # Get user
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['user'] = request.user

        ### REMOVE THIS!!! JUST FOR TESTING PURPOSES ###
        if settings.DEBUG:
            validated_data['user'] = User.objects.all().first()
        ###

        order = super(OrderSerializer, self).create(validated_data)

        return order


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        exclude = ['modified_date']
