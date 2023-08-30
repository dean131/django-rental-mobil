from .views import CarModelViewSet, RentalModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('cars', CarModelViewSet, basename='car')
router.register('rentals', RentalModelViewSet,  basename='rental')

urlpatterns = router.urls
