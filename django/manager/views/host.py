# Third party imports
from rest_framework.permissions import IsAuthenticated

# Project imports
from manager.models import Host
from manager.serializers import HostSerializer
from shared.views import BaseCollectionViewSet


class HostViewSet(BaseCollectionViewSet):
    """ A ViewSet for Host. """
    model_class = Host
    queryset = model_class.objects.all()
    serializer_class = HostSerializer
    http_method_names = ('get', 'post')
    search_fields = ('name',)
    serializers = {
        'default': serializer_class,
    }
    permission_classes = [IsAuthenticated]
