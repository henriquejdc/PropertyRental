from manager.models import HostCommission, OwnerCommission, SeazoneCommission
from model_bakery import baker

from django.test import TestCase


class ModelsStrTestCase(TestCase):
    """All tests for to get __str__ methods from models."""

    def setUp(self) -> None:
        self.maxDiff = None
        return super().setUp()

    def test_get_str_model(self):
        """Test all models __str__ methods."""

        owner = baker.make("manager.Owner")
        self.assertEqual(str(owner), owner.__str__())

        host = baker.make("manager.Host")
        self.assertEqual(str(host), host.__str__())

        property_obj = baker.make(
            "manager.Property",
            owner=owner,
            host=host,
        )
        self.assertEqual(str(property_obj), property_obj.__str__())

        reservation = baker.make("manager.Reservation", property=property_obj)
        self.assertEqual(str(reservation), reservation.__str__())

        seazone_commission = SeazoneCommission.objects.get(
            reservation=reservation
        )
        self.assertEqual(str(seazone_commission), seazone_commission.__str__())

        host_commission = HostCommission.objects.get(reservation=reservation)
        self.assertEqual(str(host_commission), host_commission.__str__())

        owner_commission = OwnerCommission.objects.get(reservation=reservation)
        self.assertEqual(str(owner_commission), owner_commission.__str__())
