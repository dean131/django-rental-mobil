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
        elif self.action == 'retrieve':
            return CarModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        fields = request.query_params.getlist('fields')
        if fields:
            fields = fields[0].split(',')
        serializer = self.get_serializer(queryset, fields=fields, many=True)
        return Response(serializer.data)


class RentalModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Rental.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RentalDynamicFieldsModelSerializer 
        elif self.action == 'retrieve':
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

