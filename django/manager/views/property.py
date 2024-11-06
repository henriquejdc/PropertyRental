# Django imports
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Third party imports
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Project imports
from manager.filters import PropertyFilter
from manager.models import Property, Reservation
from manager.serializers import PropertySerializer, PropertyCreateSerializer
from shared.views import BaseCollectionViewSet


class PropertyViewSet(BaseCollectionViewSet):
    """ A ViewSet for Property. """
    model_class = Property
    queryset = model_class.objects.all()
    serializer_class = PropertySerializer
    http_method_names = ('get', 'post')
    search_fields = ('title',)
    serializers = {
        'default': serializer_class,
        'create': PropertyCreateSerializer,
    }
    permission_classes = [IsAuthenticated]
    filterset_class = PropertyFilter

    @swagger_auto_schema(
        operation_summary="Availability properties",
        manual_parameters=[
            openapi.Parameter(
                'property_id', openapi.IN_QUERY, description="Property ID", type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'start_date', openapi.IN_QUERY, description="Start date (format YYYY-MM-DD)",
                type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY, description="End date (format YYYY-MM-DD)",
                type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'guests_quantity', openapi.IN_QUERY, description="Guests quantity", type=openapi.TYPE_INTEGER,
                required=True
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def availability(self, request):
        property_id = request.GET.get('property_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        guests_quantity = request.GET.get('guests_quantity')

        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': _('Property not found')})

        if property_obj.capacity < int(guests_quantity):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('Property does not have capacity')}
            )

        overlapping_reservations = Reservation.objects.filter(
            property=property_obj,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()
        if overlapping_reservations:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('Not avalailable for the selected dates.')}
            )

        return Response(
            status=status.HTTP_200_OK,
            data={'message': _('Avalailable for the selected dates.')}
        )