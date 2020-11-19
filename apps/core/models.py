from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .behaviours import Timestampable


CURRENCY_TYPES = [
    ('crypto', "Crypto"),
    ('fiat', "Fiat")
]


class Currency(models.Model):
    name = models.CharField(max_length=64)
    verbose_name = models.CharField(max_length=64)
    acronym = models.CharField(max_length=8)
    currency_type = models.CharField(max_length=16, choices=CURRENCY_TYPES)

    def __str__(self):
        return self.verbose_name


class User(AbstractUser):
    pass


class UserBalance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    balance = models.DecimalField(max_digits=64, decimal_places=5)


ORDER_TYPES = [
    ('sell', "Sell"),
    ('buy', "Buy")
]


class Order(Timestampable, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    origin_currency = models.ForeignKey(Currency, related_name='origin_orders', 
                                        on_delete=models.CASCADE)
    destination_currency = models.ForeignKey(Currency, related_name='destination_orders',
                                             on_delete=models.CASCADE)

    order_type = models.CharField(max_length=16, choices=ORDER_TYPES)
    price = models.DecimalField(max_digits=64, decimal_places=5)


class Trade(Timestampable, models.Model):
    buyer_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='buyer_trades')
    seller_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='seller_trades')
