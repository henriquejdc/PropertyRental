# Django imports
from django.db.models import Sum, Count
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Third party imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

# Project imports
from manager.models import Property, SeazoneCommission, HostCommission, OwnerCommission


class CommissionViewSet(viewsets.ViewSet):
    """ A ViewSet for Financial. """


    @swagger_auto_schema(
        operation_summary="Financial commission",
        manual_parameters=[
            openapi.Parameter(
                'type', openapi.IN_QUERY, description="Type 'seazone', 'owner', 'host", type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'month', openapi.IN_QUERY, description="Month MM",
                type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'year', openapi.IN_QUERY, description="Month YYYYY",
                type=openapi.TYPE_STRING, required=False
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        commission_type = request.query_params.get('type', None)
        month = request.query_params.get('month', None)
        year = request.query_params.get('year', None)

        if not commission_type or commission_type not in ['seazone', 'owner', 'host']:
            raise ValidationError(_("Use type 'seazone', 'owner' or 'host'."))

        if (year and not month) or (month and not year):
            raise ValidationError(
                _("Required year and month.")
            )

        filter = {}
        if month and year:
            filter = {
                'reservation_date__year': year,
                'reservation_date__month': month
            }

        if commission_type == 'seazone':
            commissions = SeazoneCommission.objects.filter(**filter)
        elif commission_type == 'host':
            commissions = HostCommission.objects.filter(**filter)
        elif commission_type == 'owner':
            commissions = OwnerCommission.objects.filter(**filter)

        total_commission = commissions.aggregate(total_commission=Sum('commission_value'))['total_commission'] or 0
        total_reservations = commissions.aggregate(total_reservations=Count('id'))['total_reservations'] or 0

        properties_statement = []
        for property in Property.objects.all():
            property_commissions = commissions.filter(reservation__property=property)
            total_property_commission = property_commissions.aggregate(
                total_commission=Sum('commission_value')
            )['total_commission'] or 0
            total_property_reservations = property_commissions.aggregate(
                total_reservations=Count('id')
            )['total_reservations'] or 0
            properties_statement.append({
                'property_id': property.id,
                'total_commission': total_property_commission,
                'total_reservations': total_property_reservations
            })

        data = {
            'total_commission': total_commission,
            'total_reservations': total_reservations,
            'properties_statement': properties_statement
        }

        return Response(data, status=status.HTTP_200_OK)
