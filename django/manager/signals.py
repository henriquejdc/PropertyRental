from decimal import Decimal


def generate_commissions(sender, instance, created, **kwargs):
    from manager.models import SeazoneCommission, HostCommission, OwnerCommission

    if created:
        property_instance = instance.property
        total_price = instance.total_price
        reservation_date = instance.end_date

        seazone_commission_value = total_price * Decimal(property_instance.seazone_commission)
        SeazoneCommission.objects.create(
            reservation=instance,
            reservation_date=reservation_date,
            commission_percent=property_instance.seazone_commission,
            commission_value=seazone_commission_value
        )

        host_commission_value = total_price * Decimal(property_instance.host_commission)
        HostCommission.objects.create(
            reservation=instance,
            reservation_date=reservation_date,
            commission_percent=property_instance.host_commission,
            commission_value=host_commission_value,
            host=property_instance.host
        )

        owner_commission_percent = 1 - (property_instance.seazone_commission + property_instance.host_commission)
        owner_commission_value = total_price - (seazone_commission_value + host_commission_value)
        OwnerCommission.objects.create(
            reservation=instance,
            reservation_date=reservation_date,
            commission_percent=owner_commission_percent,
            commission_value=owner_commission_value,
            owner=property_instance.owner
        )
