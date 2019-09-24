import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DevopsCapacityTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('devops-capacity')

    def test_calculate_capacity(self):
        payload = {
            'DM_capacity': 4,
            'DE_capacity': 7,
            'data_centers':
            [
                {'name': 'Rome', 'servers': 22},
                {'name': 'Riga', 'servers': 8},
                {'name': 'Berlin', 'servers': 61}
            ]
        }
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), {'DE': 14, 'DM_data_center': 'Rome'})

    def test_empty_data_centers_list(self):
        payload = {
            'DM_capacity': 5,
            'DE_capacity': 3,
            'data_centers': []
        }
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {'data_centers': ['This list may not be empty.']})

    def test_invalid_capacity(self):
        payload = {
            'DM_capacity': 'qwerty',
            'DE_capacity': 1,
            'data_centers': [{'name': 'Riga', 'servers': 8}]
        }
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {'DM_capacity': ['A valid integer is required.']})

    def test_negative_capacity(self):
        payload = {
            'DM_capacity': -2,
            'DE_capacity': 1,
            'data_centers': [{'name': 'Riga', 'servers': 8}]
        }
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {'DM_capacity': ['Ensure this value is greater than or equal to 1.']})

    def test_zero_servers(self):
        payload = {
            'DM_capacity': 4,
            'DE_capacity': 7,
            'data_centers':
            [
                {'name': 'Rome', 'servers': 0},
                {'name': 'Riga', 'servers': 8}
            ]
        }
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), {'DE': 1, 'DM_data_center': 'Riga'})
