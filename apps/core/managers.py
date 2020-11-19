from django.db import models

from .querysets import UserBalanceQuerySet


class UserBalanceManager(models.Manager):
    def get_queryset(self, user):
        qs = UserBalanceQuerySet(self.model, using=self._db)
        return qs.filter(user_id=user.id)
