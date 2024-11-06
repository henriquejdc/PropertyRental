# Django imports
from django.utils import timezone

# Third-party imports
from rest_framework import serializers

# Project imports
from manager.models import (
    Property,
    Owner,
    Host,
    Reservation,
    SeazoneCommission,
    HostCommission,
    OwnerCommission
)


class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields = '__all__'


class HostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Host
        fields = '__all__'



class PropertySerializer(serializers.ModelSerializer):

    host = HostSerializer()
    owner = OwnerSerializer()

    class Meta:
        model = Property
        fields = '__all__'



class PropertyOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        exclude = ('owner', 'host')


class PropertyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = '__all__'

    def validate(self, data):
        seazone_commission = data.get('seazone_commission', 0)
        host_commission = data.get('host_commission', 0)
        owner_commission = data.get('owner_commission', 0)

        total_commission = seazone_commission + host_commission + owner_commission
        if total_commission != 1:
            raise serializers.ValidationError(
                "The sum of seazone_commission, host_commission, and owner_commission must equal 1."
            )

        return data


class ReservationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = (
            'property',
            'client_name',
            'client_email',
            'start_date',
            'end_date',
            'guests_quantity',
        )

    def validate_start_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("The start date must be in the future.")
        return value

    def validate_end_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("The end date must be in the future.")
        return value

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if end_date <= start_date:
            raise serializers.ValidationError("The end date must be after the start date.")

        property = data.get('property')
        guests_quantity = data.get('guests_quantity')
        if guests_quantity > property.capacity:
            raise serializers.ValidationError("The number of guests exceeds the maximum capacity of the property.")

        overlapping_reservations = Reservation.objects.filter(
            property=property,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()
        if overlapping_reservations:
            raise serializers.ValidationError("The property is not available for the selected dates.")

        return data


class ReservationSerializer(serializers.ModelSerializer):

    property = PropertyOnlySerializer()
    owner = serializers.SerializerMethodField()
    host = serializers.SerializerMethodField()
    seazone_commission = serializers.SerializerMethodField()
    host_commission = serializers.SerializerMethodField()
    owner_commission = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = '__all__'

    @staticmethod
    def get_owner(obj):
        return OwnerSerializer(obj.property.owner).data

    @staticmethod
    def get_host(obj):
        return HostSerializer(obj.property.host).data

    @staticmethod
    def get_seazone_commission(obj):
        return SeazoneCommission.objects.get(reservation=obj).commission_value

    @staticmethod
    def get_host_commission(obj):
        return HostCommission.objects.get(reservation=obj).commission_value

    @staticmethod
    def get_owner_commission(obj):
        return OwnerCommission.objects.get(reservation=obj).commission_value


class CommissionSummarySerializer(serializers.Serializer):
    property_id = serializers.IntegerField()
    total_commission = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_reservations = serializers.IntegerField()


class CommissionTotalSerializer(serializers.Serializer):
    total_commission = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_reservations = serializers.IntegerField()
    property_details = CommissionSummarySerializer(many=True)
