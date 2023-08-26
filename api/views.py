from datetime import datetime
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    CarModelSerializer, 
    CarDynamicFieldsModelSerializer, 
    RentalModelSerializer,
    RentalDynamicFieldsModelSerializer,
)

from base.models import Car, Rental


class CarModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Car.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CarDynamicFieldsModelSerializer 
        else:
            return CarModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        fields = request.query_params.getlist('fields')
        if fields:
            fields = fields[0].split(',')
        else:
            fields = [
                'name',
                'car_type',
                'price',
                'color',
                'transmission',
                'license_plate',
                'passenger_capacity',
                'fuel_capacity',
                'description',
                'picture',
            ]
        serializer = self.get_serializer(queryset, fields=fields, many=True)
        return Response(serializer.data)


class RentalModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Rental.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RentalDynamicFieldsModelSerializer 
        else:
            return RentalModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        fields = request.query_params.getlist('fields')
        if fields:
            fields = fields[0].split(',')
        else:
            fields = [
            'id',
            'customer', 
            'car', 
            'status', 
            'start_date', 
            'end_date', 
            'total_cost', 
            'total_days',
        ]
        serializer = self.get_serializer(queryset, fields=fields, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user = request.user

        car_id = request.data.get('car')
        car = Car.objects.get(id=car_id) 

        if car.is_booked == True:
            return Response({
                'status': 'error',
                'message': 'Car is Booked',
            })

        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(start_date, date_format).date()
        end_date = datetime.strptime(end_date, date_format).date()

        rental = Rental.objects.create(
            customer=user, 
            car=car, 
            start_date=start_date, 
            end_date=end_date,
        )
        rental.save()

        car.is_booked = True
        car.save()

        serializer = self.get_serializer(rental)
        return Response(serializer.data)
