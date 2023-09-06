from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CarModelSerializer, 
    CarDynamicFieldsModelSerializer, 
    RentalModelSerializer,
    RentalDynamicFieldsModelSerializer,
)

from base.models import Car, Rental
from .filters import CarListFilter, RentalListFilter
from rental_mobil.my_libraries import CustomResponse


class CarModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Car.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarListFilter
    search_fields = [
        'name', 
        'car_type', 
        'color', 
        'description', 
        'transmission',
    ]

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return CarDynamicFieldsModelSerializer 
        else:
            return CarModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        fields = request.query_params.getlist('fields')
        if fields:
            fields = fields[0].split(',')

        context = {
            'fields': fields,
            'request': request,
        }
        serializer = self.get_serializer(queryset, many=True, context=context)
        return CustomResponse.success(
            message='Car list retrieved successfully.',
            data=serializer.data,
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        fields = request.query_params.getlist('fields')
        if fields:
            fields = fields[0].split(',')

        context = {
            'fields': fields,
            'request': request,
        }
        serializer = self.get_serializer(instance, context=context)
        return CustomResponse.success(
            message='Car retrieved successfully.',
            data=serializer.data,
        )
    
    def partial_update(self, request, *args, **kwargs):
        car = self.get_object()
        serializer = CarModelSerializer(car, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                message='Car update successful.',
                data=serializer.data,
            )
        else:
            return CustomResponse.error(
                message='Car update failed.',
                error=serializer.errors,
            )


class RentalModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Rental.objects.all()

    filter_backends = [DjangoFilterBackend,]
    filterset_class = RentalListFilter

    def get_serializer_class(self):
        if self.action == 'list' or 'retrive':
            return RentalDynamicFieldsModelSerializer 
        elif self.action == 'create':
            return RentalModelSerializer
        else:
            return RentalModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        fields = request.query_params.getlist('fields')
        if fields:
            fields = fields[0].split(',')

        child_fields = request.query_params.getlist('child_fields')
        if child_fields:
            child_fields = child_fields[0].split(',')

        context = {
            'child_fields': child_fields,
            'fields': fields,
            'request': request,
        }
        serializer = self.get_serializer(queryset, many=True, context=context)
        return CustomResponse.success(
            message='List of rentals retrieved successfully.',
            data=serializer.data,
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        fields = request.query_params.getlist('fields')
        if fields:
            fields = fields[0].split(',')

        child_fields = request.query_params.getlist('child_fields')
        if child_fields:
            child_fields = child_fields[0].split(',')
            
        context = {
            'child_fields': child_fields,
            'fields': fields,
            'request': request,
        }
        serializer = self.get_serializer(instance, context=context)
        return CustomResponse.success(
            message='Rental retrieved successfully.',
            data=serializer.data,
        )
    
    def create(self, request, *args, **kwargs):
        user = request.user

        car_id = request.data.get('car')
        car = Car.objects.get(id=car_id) 

        if car.is_booked == True:
            return CustomResponse.error(
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

        serializer = RentalModelSerializer(rental)
        return CustomResponse.success(
            message='Rental successful.',
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )
