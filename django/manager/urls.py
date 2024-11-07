from manager.views.financial import CommissionViewSet
from manager.views.host import HostViewSet
from manager.views.owner import OwnerViewSet
from manager.views.property import PropertyViewSet
from manager.views.reservation import ReservationViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"properties", PropertyViewSet, basename="property")
router.register(r"hosts", HostViewSet, basename="host")
router.register(r"owners", OwnerViewSet, basename="owner")
router.register(r"reservations", ReservationViewSet, basename="reservation")
router.register(
    r"financial/commissions", CommissionViewSet, basename="financial"
)
urlpatterns = router.urls
