# Django imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Project imports
from manager.signals import generate_commissions
from shared.models import BaseModelDate


class Owner(BaseModelDate):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Host(BaseModelDate):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Property(BaseModelDate):
    title = models.CharField(max_length=200)
    address_street = models.CharField(max_length=200)
    address_number = models.CharField(max_length=200)
    address_neighborhood = models.CharField(max_length=200)
    address_city = models.CharField(max_length=200)
    country = models.CharField(max_length=3)
    rooms = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='properties')
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='properties')
    seazone_commission = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    host_commission = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    owner_commission = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return self.title

class StatusChoices(models.TextChoices):
    CONFIRMED = 'Confirmed', _('Confirmed')
    CANCELLED = 'Cancelled', _('Cancelled')

class Reservation(BaseModelDate):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reservations")
    start_date = models.DateField()
    end_date = models.DateField()
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    guests_quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.CONFIRMED
    )

    def __str__(self):
        return f'{self.property} - {self.client_name}'

    def save(self, *args, **kwargs):
        nights = (self.end_date - self.start_date).days
        self.total_price = self.property.price_per_night * nights
        super().save(*args, **kwargs)


class SeazoneCommission(BaseModelDate):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="seazone_commission")
    reservation_date = models.DateField()
    commission_percent = models.FloatField()
    commission_value = models.DecimalField(max_digits=10, decimal_places=2)


class HostCommission(BaseModelDate):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="host_commission")
    reservation_date = models.DateField()
    commission_percent = models.FloatField()
    commission_value = models.DecimalField(max_digits=10, decimal_places=2)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)


class OwnerCommission(BaseModelDate):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="owner_commission")
    reservation_date = models.DateField()
    commission_percent = models.FloatField()
    commission_value = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)


models.signals.post_save.connect(generate_commissions, sender=Reservation)