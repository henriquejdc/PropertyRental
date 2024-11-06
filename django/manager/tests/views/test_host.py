# Base imports
from typing import List

# Django imports
from django.urls import reverse

# Third party imports
from model_bakery import baker


# Project imports
from shared.tests import BaseAPITestCase


class HostViewSetTestCase(BaseAPITestCase):
    """Test all scenarios for HostViewSet."""

    tests_to_perform: List = [
        'create_ok',
        'create_validation_error',
        'list',
        'retrieve',
    ]

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("host-list")
        self.row_object = baker.make(
            'manager.Host',
            name='Item1'
        )
        self.row_object_two = baker.make(
            'manager.Host',
            name='Item2'
        )
        self.validation_error_column = 'name'
        self.post_data = {
            "name": "Item3",
            "email": "user@example.com",
            "phone": "string"
        }
        self.total_rows = 2
        self.http_404_error_description = 'No Host matches the given query.'

    def set_test_retrieve_fields(self):
        self.retrieve_test_fields = {
            "name": self.row_object.name,
            "email": self.row_object.email,
            "phone": self.row_object.phone
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
