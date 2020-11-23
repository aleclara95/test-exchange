import django_filters

from .models import Order, Trade, UserBalance


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class UserBalanceFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__username')
    currency = CharInFilter(field_name='currency__acronym', lookup_expr='in')

    class Meta:
        model = UserBalance
        fields = ['user', 'currency']
    pass


class OrderFilter(django_filters.FilterSet):
    origin = django_filters.CharFilter(field_name='currency_pair__origin__acronym')
    destination = django_filters.CharFilter(field_name='currency_pair__destination__acronym')
    exclude_user = django_filters.CharFilter(field_name='user__username', exclude=True)

    o = django_filters.OrderingFilter(
        fields=(('price', 'price'),),field_labels={'price': 'Price'}
    )

    class Meta:
        model = Order
        fields = ['origin', 'destination', 'is_active', 'exclude_user']


class TradeFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(('create_date', 'create_date'),),field_labels={'create_date': 'Create date'}
    )

    class Meta:
        model = Trade
        fields = ['o']
