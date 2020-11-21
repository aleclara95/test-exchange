from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F

from . import behaviours


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


class CurrencyPair(models.Model):
    origin = models.ForeignKey(Currency, on_delete=models.CASCADE,
                               related_name='origin_currency_pairs')
    destination = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                    related_name='destination_currency_pairs')

    class Meta:
        unique_together = ['origin', 'destination']

    def __str__(self):
        return f"{self.origin.acronym}/{self.destination.acronym}"


class User(AbstractUser):
    pass


class UserBalance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_balances')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    balance = models.DecimalField(max_digits=64, decimal_places=settings.MAX_DECIMAL_PLACES)

    class Meta:
        unique_together = ['user', 'currency']

    def __str__(self):
        return f"Balance - {self.user} | {self.currency}"

    def save(self, *args, **kwargs):
        # Round money to 2 decimals if it's a fiat currency
        if self.currency.currency_type == 'fiat':
            self.balance = round(self.balance, settings.FIAT_DECIMAL_PLACES)

        super(UserBalance, self).save(*args, **kwargs)


ORDER_TYPES = [
    ('sell', "Sell"),
    ('buy', "Buy")
]


class Order(behaviours.Timestampable, behaviours.Activable, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.CASCADE)

    order_type = models.CharField(max_length=16, choices=ORDER_TYPES)
    price = models.DecimalField(max_digits=64, decimal_places=settings.MAX_DECIMAL_PLACES)
    original_amount = models.DecimalField(max_digits=64, decimal_places=settings.MAX_DECIMAL_PLACES)
    amount = models.DecimalField(max_digits=64, decimal_places=settings.MAX_DECIMAL_PLACES)

    def __str__(self):
        return f"""{self.order_type} | {self.currency_pair.origin.acronym}/{self.currency_pair.destination.acronym}
                Order | {self.create_date.strftime(settings.DEFAULT_DATETIME_FORMAT)} | {self.user}"""

    def save(self, *args, **kwargs):
        # Get the value rounded to 2 decimals if it's a fiat currency
        if self.currency_pair.origin.currency_type == 'fiat':
            self.price = round(self.price, settings.FIAT_DECIMAL_PLACES)

        if self.pk is None:
            if self.order_type == 'buy':
                other_order_type = 'sell'
                order_by = 'price'
                price_filter_key = 'price__lte'
                self_currency = self.currency_pair.destination
                other_currency = self.currency_pair.origin

            else:
                other_order_type = 'buy'
                order_by = '-price'
                price_filter_key = 'price__gte'
                self_currency = self.currency_pair.origin
                other_currency = self.currency_pair.destination

            # Check if order can be put
            try:
                current_balance = self.user.user_balances.filter(currency=self_currency).first().balance
            except AttributeError:
                import pdb; pdb.set_trace()
                raise Exception("There's no UserBalance object created for that currency")

            filter_obj = {
                'order_type': other_order_type,
                'currency_pair': self.currency_pair,
                'is_active': True
            }

            filter_obj[price_filter_key] = self.price

            matching_order = Order.objects.annotate(total=F('price') * F('amount')) \
                                          .filter(**filter_obj) \
                                          .exclude(user=self.user) \
                                          .order_by(order_by).first()

            if self.order_type == 'buy':
                buy_required = self.amount * self.price

                if buy_required > current_balance:
                    # The ideal here would be to make a custom exception
                    raise Exception("There are not sufficient funds")

            elif self.order_type == 'sell':
                sell_required = self.amount

                if sell_required > current_balance:
                    # The ideal here would be to make a custom exception
                    raise Exception("There are not sufficient funds")

            super(Order, self).save(*args, **kwargs)

            if matching_order:
                # There's a matching order. Then, create trade object and update orders
                buyer_order = self if self.order_type == 'buy' else matching_order
                seller_order = matching_order if self.order_type == 'buy' else self

                # Update self order and balances
                self_origin_balance = self.user.user_balances.filter(currency=self.currency_pair.origin).first()
                self_destination_balance = self.user.user_balances.filter(currency=self.currency_pair.destination).first()

                if not self_origin_balance or not self_destination_balance:
                    raise Exception("There's no UserBalance object created for that currency")

                amount = min([self.amount, matching_order.amount])
                total = min([amount * self.price, amount * matching_order.price])
                
                if self.order_type == 'buy':
                    self_origin_balance.balance += amount
                    self_destination_balance.balance -= total

                elif self.order_type == 'sell':
                    self_origin_balance.balance -= amount
                    self_destination_balance.balance += total

                self.amount -= amount
                if self.amount <= 0:
                    self.is_active = False

                self_origin_balance.save()
                self_destination_balance.save()

                # Update matching order and balances
                matching_order_origin_balance = matching_order.user.user_balances \
                                                                 .filter(currency=self.currency_pair.origin) \
                                                                 .first()
                matching_order_destination_balance = matching_order.user.user_balances \
                                                                 .filter(currency=self.currency_pair.destination) \
                                                                 .first()

                if not matching_order_origin_balance or not matching_order_destination_balance:
                    raise Exception("There's no UserBalance object created for that currency")

                if matching_order.order_type == 'buy':
                    matching_order_origin_balance.balance += amount
                    matching_order_destination_balance.balance -= total

                elif matching_order.order_type == 'sell':
                    matching_order_origin_balance.balance -= amount
                    matching_order_destination_balance.balance += total

                matching_order.amount -= amount
                if matching_order.amount <= 0:
                    matching_order.is_active = False

                matching_order_origin_balance.save()
                matching_order_destination_balance.save()

                # Save orders
                super(Order, self).save(*args, **kwargs)
                matching_order.save()

                # Create trade
                Trade.objects.create(buyer_order=buyer_order, seller_order=seller_order)
        else:
            super(Order, self).save(*args, **kwargs)


class Trade(behaviours.Timestampable, behaviours.Activable, models.Model):
    buyer_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='buyer_trades')
    seller_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='seller_trades')

    def __str__(self):
        origin_currency = self.seller_order.currency_pair.origin
        destination_currency = self.seller_order.currency_pair.destination
        return f"""[{self.seller_order.currency_pair}] {self.seller_order.user}
                   -> {self.buyer_order.user}
                   | {self.create_date.strftime(settings.DEFAULT_DATETIME_FORMAT)}"""
