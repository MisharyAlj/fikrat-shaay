import django_filters
from .models import Product, Invoice
from django_filters import DateFilter, CharFilter
from django.utils.translation import gettext as _


class ProductFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains', label=_('Title'))
    start_date = DateFilter(field_name='createdAt',
                            lookup_expr='gte', label=_('Start date'))
    end_date = DateFilter(field_name='createdAt',
                          lookup_expr='lte', label=_('End date'))

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('title', 'createdAt', 'summary', 'slug', 'updatedAt')


class InvoiceFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='createdAt',
                            lookup_expr='gte', label=_('Start date'))
    end_date = DateFilter(field_name='createdAt',
                          lookup_expr='lte', label=_('End date'))

    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ('uniqueId', 'createdAt', 'slug', 'updatedAt')
