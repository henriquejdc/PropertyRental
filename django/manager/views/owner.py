# Django imports
import django_filters.rest_framework

# Third party imports
from rest_framework.permissions import IsAuthenticated

# Project imports
from manager.models import Owner
from manager.serializers import OwnerSerializer
from shared.views import BaseCollectionViewSet


class OwnerViewSet(BaseCollectionViewSet):
    """ A ViewSet for Owner. """
    model_class = Owner
    queryset = model_class.objects.all()
    serializer_class = OwnerSerializer
    http_method_names = ('get', 'post')
    search_fields = ('name',)
    serializers = {
        'default': serializer_class,
    }
    permission_classes = [IsAuthenticated]
