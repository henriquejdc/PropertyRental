# Base imports
import json
from copy import deepcopy
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

# Django imports
from django.urls import reverse

# Third party imports
from rest_framework import status
from model_bakery import baker

# Project imports
from manager.serializers import PropertyOnlySerializer, OwnerSerializer, HostSerializer
from shared.tests import BaseAPITestCase


class ReservationViewSetTestCase(BaseAPITestCase):
    """Test all scenarios for ReservationViewSet."""

    tests_to_perform: List = [
        'create_ok',
        'create_validation_error',
        'list',
        'retrieve',
    ]

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("reservation-list")
        self.owner = baker.make(
            'manager.Owner',
            name='Owner'
        )
        self.host = baker.make(
            'manager.Host',
            name='Host'
        )
        self.property = baker.make(
            'manager.Property',
            title='Item1',
            host=self.host,
            owner=self.owner,
            price_per_night=Decimal(20.11),
            seazone_commission=0.1,
            owner_commission=0.7,
            host_commission=0.7,
            capacity=2
        )

        self.row_object = baker.make(
            'manager.Reservation',
            client_name='Item1',
            client_email='Item1@example.com',
            property=self.property,
            start_date=datetime.strptime('2024-01-30', '%Y-%m-%d').date(),
            end_date=datetime.strptime('2024-03-30', '%Y-%m-%d').date(),
        )

        self.row_object_two = baker.make(
            'manager.Reservation',
            client_name='Item2',
            client_email='Item2@example.com',
            property=self.property,
            start_date=datetime.strptime('2024-04-30', '%Y-%m-%d').date(),
            end_date=datetime.strptime('2024-05-30', '%Y-%m-%d').date(),
        )
        self.validation_error_column = 'client_name'

        self.today = datetime.today().date()
        self.post_data = {
            "property": self.property.pk,
            "client_name": "Item3",
            "client_email": "Item3@example.com",
            "start_date": (self.today + timedelta(days=2)).strftime('%Y-%m-%d'),
            "end_date": (self.today + timedelta(days=7)).strftime('%Y-%m-%d'),
            "guests_quantity": 1,
        }
        self.total_rows = 2
        self.http_404_error_description = 'No Reservation matches the given query.'

    def set_test_retrieve_fields(self):
        self.retrieve_test_fields = {
            "property": PropertyOnlySerializer(self.property).data,
            "owner": OwnerSerializer(self.owner).data,
            "host": HostSerializer(self.host).data,
            "seazone_commission": 120.66,
            "host_commission": 844.62,
            "owner_commission": 241.32,
            "client_name": self.row_object.client_name,
            "client_email": self.row_object.client_email,
            "guests_quantity": self.row_object.guests_quantity,
            "start_date": '2024-01-30',
            "end_date": '2024-03-30',
            "total_price": "1206.60",
            "status": "Confirmed",
        }

    def set_test_list_scenarios(self):
        self.list_test_scenarios = [
            # Assert without pagination.
            {
                'url': self.url,
                'rows': self.total_rows,
                'field_first_row_key': 'id',
                'field_first_row_value': self.row_object.pk
            },
            # Assert search name without pagination.
            {
                'url': f'{self.url}?search=Item1',
                'rows': 1,
                'field_first_row_key': 'id',
                'field_first_row_value': self.row_object.pk
            },
            # Assert pagination page 1.
            {
                'url': f'{self.url}?page_size=1&page=1',
                'rows': 1,
                'field_first_row_key': 'id',
                'field_first_row_value': self.row_object.pk
            },
            # Assert pagination page 2.
            {
                'url': f'{self.url}?page_size=1&page=2',
                'rows': 1,
                'field_first_row_key': 'id',
                'field_first_row_value': self.row_object_two.pk
            }
        ]

    def test_reservation_date_invalid(self):
        data = deepcopy(self.post_data)
        data['start_date'] = '2024-01-30'
        data['end_date'] = '2024-03-30'
        response = self.post(
            self.url, data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertEqual(
            contents['description']['detail'],
            {
                'start_date': ['The start date must be in the future.'],
                'end_date': ['The end date must be in the future.']
            }
        )

    def test_reservation_interval_date_invalid(self):
        data = deepcopy(self.post_data)
        data.update({
            "start_date": (self.today + timedelta(days=7)).strftime('%Y-%m-%d'),
            "end_date": (self.today + timedelta(days=2)).strftime('%Y-%m-%d'),
        })
        response = self.post(
            self.url, data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertEqual(
            contents['description']['detail'],
        {"errors":["The end date must be after the start date."]}
        )

    def test_reservation_capacity_invalid(self):
        data = deepcopy(self.post_data)
        data.update({
            "guests_quantity": 1000
        })
        response = self.post(
            self.url, data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertEqual(
            contents['description']['detail'],
        {"errors":["The number of guests exceeds the maximum capacity of the property."]}
        )

    def test_reservation_not_available(self):
        data = deepcopy(self.post_data)
        response = self.post(
            self.url, data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.post(
            self.url, data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertEqual(
            contents['description']['detail'],
        {"errors":["The property is not available for the selected dates."]}
        )

