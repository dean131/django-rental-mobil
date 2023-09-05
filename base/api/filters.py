from django_filters.rest_framework import FilterSet, RangeFilter

from ..models import Car, Rental


class CarListFilter(FilterSet):
    price = RangeFilter()
    class Meta:
        model = Car
        fields = '__all__'
        exclude = ['picture',]


class RentalListFilter(FilterSet):
    class Meta:
        model = Rental
        fields = '__all__'