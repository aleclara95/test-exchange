from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from django.conf import settings

from .models import Currency, CurrencyPair, Order, Trade, User, UserBalance


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = []


class CurrencyPairSerializer(serializers.ModelSerializer):
    origin = serializers.SlugRelatedField(slug_field='acronym', read_only=True)
    destination = serializers.SlugRelatedField(slug_field='acronym', read_only=True)
    class Meta:
        model = CurrencyPair
        exclude = []


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')


class UserBalanceSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(slug_field='acronym', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    currency_type = serializers.CharField(source='currency.currency_type')
    
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

        order = super(OrderSerializer, self).create(validated_data)

        return order


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        exclude = ['modified_date']
