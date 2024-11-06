# Django imports
import django_filters.rest_framework

# Third party imports
from rest_framework.permissions import IsAuthenticated

# Project imports
from manager.filters import ReservationFilter
from manager.models import Reservation
from manager.serializers import ReservationSerializer, ReservationCreateSerializer
from shared.views import BaseCollectionViewSet


class ReservationViewSet(BaseCollectionViewSet):
    """ A ViewSet for Reservation. """
    model_class = Reservation
    queryset = model_class.objects.all()
    serializer_class = ReservationSerializer
    http_method_names = ('get', 'post')
    search_fields = ('title',)
    serializers = {
        'default': serializer_class,
        'create': ReservationCreateSerializer,
    }
    permission_classes = [IsAuthenticated]
    filterset_class = ReservationFilter
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
    )
