from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Car, Rental
from .serializers import CarSerializer, RentalSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def car_list(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def customer_list(request):
#     customers = Customer.objects.all()
#     serializer = CustomerSerializer(customers, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rental_list(request):
    rentals = Rental.objects.all()
    serializer = RentalSerializer(rentals, many=True)
    return Response(serializer.data)
