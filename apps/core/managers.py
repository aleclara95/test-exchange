from django.db import models

from .querysets import OrderQuerySet, UserBalanceQuerySet


class UserBalanceManager(models.Manager):
	pass


class OrderManager(models.Manager):
    def matching_orders(self, **kwargs):
        return self.get_queryset().matching_orders()
