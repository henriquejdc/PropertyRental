import json
from datetime import datetime
from decimal import Decimal
from typing import List

from manager.models import Host, Owner, Property, Reservation
from model_bakery import baker
from rest_framework import status
from shared.tests import BaseAPITestCase

from django.urls import reverse


class PropertyViewSetTestCase(BaseAPITestCase):
    """Test all scenarios for PropertyViewSet."""

    tests_to_perform: List[str] = []

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("financial-list")
        self.owner: Owner = baker.make("manager.Owner", name="Owner")
        self.host: Host = baker.make("manager.Host", name="Host")
        self.property: Property = baker.make(
            "manager.Property",
            title="Item1",
            host=self.host,
            owner=self.owner,
            price_per_night=Decimal(20.11),
            seazone_commission=0.1,
            owner_commission=0.7,
            host_commission=0.7,
            capacity=2,
        )

        self.reservation: Reservation = baker.make(
            "manager.Reservation",
            client_name="Item1",
            client_email="Item1@example.com",
            property=self.property,
            start_date=datetime.strptime("2024-01-30", "%Y-%m-%d").date(),
            end_date=datetime.strptime("2024-03-30", "%Y-%m-%d").date(),
        )

    def test_type_error_financial(self):
        response = self.get(f"{self.url}" "?type=teste")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_type_year_financial(self):
        response = self.get(f"{self.url}" "?type=seazone" "&year=2018")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_type_seazone(self):
        response = self.get(
            f"{self.url}" "?type=seazone" "&year=2024" "&month=03"
        )
        contents = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            contents,
            {
                "total_commission": 120.66,
                "total_reservations": 1,
                "properties_statement": [
                    {
                        "property_id": 1,
                        "total_commission": 120.66,
                        "total_reservations": 1,
                    }
                ],
            },
        )

    def test_type_owner(self):
        response = self.get(
            f"{self.url}" "?type=owner" "&year=2024" "&month=03"
        )
        contents = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            contents,
            {
                "total_commission": 241.32,
                "total_reservations": 1,
                "properties_statement": [
                    {
                        "property_id": 1,
                        "total_commission": 241.32,
                        "total_reservations": 1,
                    }
                ],
            },
        )

    def test_type_host(self):
        response = self.get(
            f"{self.url}" "?type=host" "&year=2024" "&month=03"
        )
        contents = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            contents,
            {
                "total_commission": 844.62,
                "total_reservations": 1,
                "properties_statement": [
                    {
                        "property_id": 1,
                        "total_commission": 844.62,
                        "total_reservations": 1,
                    }
                ],
            },
        )
