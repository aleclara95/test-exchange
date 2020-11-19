""" Django model behaviours

    This module implements common Django model behaviours, simplifying and unifying code.
    For more info: https://blog.kevinastone.com/django-model-behaviors
"""

from django.db import models


class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
