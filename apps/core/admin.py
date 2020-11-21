from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Currency, CurrencyPair, Order, Trade, User, UserBalance


@admin.register(User)
class UserAdmin(UserAdmin):
    model = settings.AUTH_USER_MODEL


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    model = UserBalance


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    model = Trade


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    model = Currency


@admin.register(CurrencyPair)
class CurrencyPairAdmin(admin.ModelAdmin):
    model = CurrencyPair


