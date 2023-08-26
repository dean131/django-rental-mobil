from .views import CarModelViewSet, RentaModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('cars', CarModelViewSet, basename='car')
router.register('rentals', RentaModelViewSet,  basename='rental')

urlpatterns =[

] + router.urls
