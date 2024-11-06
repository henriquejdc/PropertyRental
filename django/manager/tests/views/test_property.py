# Base imports
import json
from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from typing import List

# Django imports
from django.urls import reverse

# Third party imports
from rest_framework import status
from model_bakery import baker

# Project imports
from manager.serializers import OwnerSerializer, HostSerializer
from shared.tests import BaseAPITestCase


class PropertyViewSetTestCase(BaseAPITestCase):
    """Test all scenarios for PropertyViewSet."""

    tests_to_perform: List = [
        'create_ok',
        'create_validation_error',
        'list',
        'retrieve',
    ]

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("property-list")
        self.owner = baker.make(
            'manager.Owner',
            name='Owner'
        )
        self.host = baker.make(
            'manager.Host',
            name='Host'
        )
        self.row_object = baker.make(
            'manager.Property',
            title='Item1',
            host=self.host,
            owner=self.owner,
            price_per_night=Decimal(20.11),
            seazone_commission=0.1,
            owner_commission=0.7,
            host_commission=0.7,
            capacity=20
        )
        self.row_object_two = baker.make(
            'manager.Property',
            title='Item2',
            host=self.host,
            owner=self.owner,
            price_per_night=Decimal(100.11),
            capacity=10
        )
        self.validation_error_column = 'title'
        self.post_data = {
            "title": "Item3",
            "address_street": "Line 1",
            "address_number": "99e",
            "address_neighborhood": "Hood 1",
            "address_state": "State 1",
            "address_city": "My City",
            "country": "BRA",
            "rooms": 2,
            "capacity": 5,
            "price_per_night": "20.00",
            "seazone_commission": 0.1,
            "host_commission": 0.2,
            "owner_commission": 0.7,
            "owner": self.owner.pk,
            "host": self.host.pk
        }
        self.total_rows = 2
        self.http_404_error_description = 'No Property matches the given query.'

    def set_test_retrieve_fields(self):
        self.retrieve_test_fields = {
            "title": self.row_object.title,
            "address_street": self.row_object.address_street,
            "address_number": self.row_object.address_number,
            "address_state": self.row_object.address_state,
            "address_neighborhood": self.row_object.address_neighborhood,
            "address_city": self.row_object.address_city,
            "country": self.row_object.country,
            "rooms": self.row_object.rooms,
            "capacity": self.row_object.capacity,
            "price_per_night": '20.11',
            "seazone_commission": self.row_object.seazone_commission,
            "host_commission": self.row_object.host_commission,
            "owner_commission": self.row_object.owner_commission,
            "owner": OwnerSerializer(self.owner).data,
            "host": HostSerializer(self.host).data
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
            },
            # Assert address_neighborhood.
            {
                'url': f'{self.url}?address_neighborhood={self.row_object.address_neighborhood}',
                'rows': 1,
                'field_first_row_key': 'id',
                'field_first_row_value': self.row_object.pk
            },
            # Assert address_city.
            {
                'url': f'{self.url}?address_city={self.row_object.address_city}',
                'rows': 1,
                'field_first_row_key': 'id',
                'field_first_row_value': self.row_object.pk
            },
            # Assert address_state.
            {
                'url': f'{self.url}?address_state={self.row_object.address_state}',
                'rows': 1,
                'field_first_row_key': 'id',
                'field_first_row_value': self.row_object.pk
            },
            # Assert capacity.
            {
                'url': f'{self.url}?capacity={self.row_object.capacity}',
                'rows': 1,
                'field_first_row_key': 'id',
                'field_first_row_value': self.row_object.pk
            },
            # Assert price_per_night.
            {
                'url': f'{self.url}?price_per_night=22',
                'rows': 1,
                'field_first_row_key': 'id',
                'field_first_row_value': self.row_object.pk
            },
        ]
        
    def test_not_found_property_availability(self):
        url = reverse('property-list')
        params = {
            'property_id': 9999,
            'start_date': '2024-01-01',
            'end_date': '2024-02-01',
            'guests_quantity': 1,
        }
        response = self.get(
            f'{url}availability/'
            f'?property_id={params["property_id"]}'
            f'&start_date={params["start_date"]}'
            f'&end_date={params["end_date"]}'
            f'&guests_quantity={params["guests_quantity"]}'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_capacity_availability(self):
        url = reverse('property-list')
        params = {
            'property_id': self.row_object.pk,
            'start_date': '2024-01-01',
            'end_date': '2024-02-01',
            'guests_quantity': 300,
        }
        response = self.get(
            f'{url}availability/'
            f'?property_id={params["property_id"]}'
            f'&start_date={params["start_date"]}'
            f'&end_date={params["end_date"]}'
            f'&guests_quantity={params["guests_quantity"]}'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_availability_ok(self):
        url = reverse('property-list')
        params = {
            'property_id': self.row_object.pk,
            'start_date': '2024-01-01',
            'end_date': '2024-02-01',
            'guests_quantity': 1,
        }
        response = self.get(
            f'{url}availability/'
            f'?property_id={params["property_id"]}'
            f'&start_date={params["start_date"]}'
            f'&end_date={params["end_date"]}'
            f'&guests_quantity={params["guests_quantity"]}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_availability(self):
        baker.make(
            'manager.Reservation',
            property=self.row_object,
            start_date=datetime.strptime('2024-01-30', '%Y-%m-%d').date(),
            end_date=datetime.strptime('2024-03-30', '%Y-%m-%d').date(),
        )
        url = reverse('property-list')
        params = {
            'property_id': self.row_object.pk,
            'start_date': '2024-01-01',
            'end_date': '2024-02-01',
            'guests_quantity': 1,
        }
        response = self.get(
            f'{url}availability/'
            f'?property_id={params["property_id"]}'
            f'&start_date={params["start_date"]}'
            f'&end_date={params["end_date"]}'
            f'&guests_quantity={params["guests_quantity"]}'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_property_invalid_commission(self):
        data = deepcopy(self.post_data)
        data['seazone_commission'] = 1
        response = self.post(
            self.url, data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertEqual(
            contents['description']['detail'],
        {"errors":["The sum of seazone_commission, host_commission, and owner_commission must equal 1."]}
        )
