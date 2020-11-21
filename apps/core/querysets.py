from django.db import models


class UserBalanceQuerySet(models.QuerySet):
    pass


class OrderQuerySet(models.QuerySet):
    def matching_orders(self, **kwargs):
        pass
        # return self.filter()
