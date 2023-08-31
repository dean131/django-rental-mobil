from django_filters.rest_framework import FilterSet, RangeFilter

from ..models import Car

class CarListFilter(FilterSet):
    price = RangeFilter()
    class Meta:
        model = Car
        fields = ['price']