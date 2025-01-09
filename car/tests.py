from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from car.models import Car
# Create your tests here.
class CarTestCase(APITestCase):
    def setUp(self):
        Car.objects.create(name='car1', color='red', brand='audi')
        Car.objects.create(name='car2', color='blue', brand='bmw')
        Car.objects.create(name='car3', color='green', brand='benz')
    def test_get_all_cars(self):
        url = reverse('car-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_create_car(self):
        url = reverse('car-list-create')
        data = {
            'name': 'audi',
            'color': 'yellow',
            'brand': 'audi'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_update_car(self):
        url = reverse('car-update-delete', args=[1])
        data = {
            'name': 'car1',
            'color': 'black',
            'brand': 'audi'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_car(self):
        url = reverse('car-update-delete', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)