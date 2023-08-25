from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Car, Rental
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from .serializers import CarSerializer, RentalSerializer, HomePageViewlSerializer

from base.models import Car

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

class HomePageView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = HomePageViewlSerializer(cars, many=True)
        return Response(serializer.data)
