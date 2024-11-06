# Base imports
import django_filters.rest_framework

# Project imports
from manager.models import Property, Reservation


class PropertyFilter(django_filters.FilterSet):
    property_id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')
    address_neighborhood = django_filters.CharFilter(field_name='address_neighborhood', lookup_expr='icontains')
    address_city = django_filters.CharFilter(field_name='address_city', lookup_expr='icontains')
    address_state = django_filters.CharFilter(field_name='address_state', lookup_expr='icontains')
    capacity = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    price_per_night = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')

    class Meta:
        model = Property
        fields = ['property_id', 'address_neighborhood', 'address_city', 'address_state', 'capacity', 'price_per_night']


class ReservationFilter(django_filters.FilterSet):
    property_id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')
    host_id = django_filters.NumberFilter(field_name='property__host__id', lookup_expr='exact')
    owner_id = django_filters.NumberFilter(field_name='property__owner__id', lookup_expr='exact')

    class Meta:
        model = Reservation
        fields = ['property_id', 'host_id', 'owner_id']
