from rest_framework import serializers
from base.models import (
    Car, 
    Customer, 
    Rental
    )


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['customer', 'car', 'status', 'start_date', 'end_date', 'total_cost', 'total_days',]


