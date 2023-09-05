from rest_framework import serializers
from base.models import (
    Car, 
    Rental
)


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        
class CarDynamicFieldsModelSerializer(CarModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.context['fields']

        if len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class RentalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = [
            'id',
            'customer', 
            'car', 
            'status', 
            'start_date', 
            'end_date', 
            'total_cost', 
            'total_days',
            'late_fee',
        ]


class RentalDynamicFieldsModelSerializer(RentalModelSerializer):
    car = serializers.SerializerMethodField('get_car')
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.context['fields']

        if len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_car(self, obj):
        context = {
            'fields': self.context['child_fields']
        }
        return CarDynamicFieldsModelSerializer(instance=obj.car, context=context).data

    


    


