from datetime import datetime
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CarModelSerializer, 
    CarDynamicFieldsModelSerializer, 
    RentalModelSerializer,
    RentalDynamicFieldsModelSerializer,
)

from base.models import Car, Rental
from rental_mobil.utils import custom_response


class CarModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Car.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name', 
        'car_type', 
        'color', 
        'description', 
        'transmission',
    ]

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
                'id',
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
        return custom_response(
            success=1,
            message='Car list retrieved successfully.',
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(
            success=1,
            message='Car retrieved successfully.',
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


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
        return custom_response(
            success=1,
            message='List of rentals retrieved successfully.',
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(
            success=1,
            message='Rental retrieved successfully.',
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
    
    def create(self, request, *args, **kwargs):
        user = request.user

        car_id = request.data.get('car')
        car = Car.objects.get(id=car_id) 

        if car.is_booked == True:
            return custom_response(
                success=1,
                message='The car is currently being booked by another user.',
                error='car booking',
                status_code=status.HTTP_403_FORBIDDEN,
            )

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
        return custom_response(
            success=1,
            message='Rental successful.',
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )
