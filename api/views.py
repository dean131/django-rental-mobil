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
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        fields = request.query_params.getlist('fields') 
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
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        fields = request.query_params.getlist('fields') 
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, fields=fields, many=True)
        return Response(serializer.data)

