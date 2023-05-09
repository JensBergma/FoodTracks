from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Address, Store, OpeningHours
from .serializer import AddressSerializer, StoreSerializer, OpeningHoursSerializer


class AddressListCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='tester', email='test@test.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

        self.address_data = {
            'street': 'Test Street',
            'houseNumber': '123',
            'location': 'Test City',
            'postcode': '12345'
        }
        self.response = self.client.post(
            reverse('address-list-create'),
            data=self.address_data,
            format='json'
        )

    def test_create_address(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.get().street, 'Test Street')

    def test_get_address_list(self):
        response = self.client.get(reverse('address-list-create'))
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AddressRetrieveUpdateDestroyViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='tester', email='test@test.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

        self.address = Address.objects.create(
            street='Test Street', houseNumber='123', location='Test City', postcode='12345')
        self.address_data = {
            'street': 'Updated Test Street',
            'houseNumber': '123',
            'location': 'Updated Test City',
            'postcode': '12345'
        }
        self.response = self.client.put(
            reverse('address-retrieve-update-destroy',
                    kwargs={'pk': self.address.pk}),
            data=self.address_data,
            format='json'
        )

    def test_update_address(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(Address.objects.get().street, 'Updated Test Street')

    def test_update_address_invalid_houseNumber(self):
        self.address_data['houseNumber'] = '55555555555555555'
        response = self.client.put(
            reverse('address-retrieve-update-destroy',
                    kwargs={'pk': self.address.pk}),
            data=self.address_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_address(self):
        response = self.client.delete(
            reverse('address-retrieve-update-destroy', kwargs={'pk': self.address.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Address.objects.count(), 0)


class OpeningHoursListCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='tester', email='test@test.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        self.url = reverse('opening-hours-list-create')

    def test_create_opening_hours(self):
        data = {
            'dayOfWeek': 1,
            'openingTime': '08:00',
            'closingTime': '17:00',
            'isClosed': False,
            'isSpecialTime': False
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OpeningHours.objects.count(), 1)

    def test_get_opening_hours_list(self):
        response = self.client.get(reverse('opening-hours-list-create'))
        openingHours = OpeningHours.objects.all()
        serializer = OpeningHoursSerializer(openingHours, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OpeningHoursRetrieveUpdateDestroyViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='tester', email='test@test.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        self.opening_hours = OpeningHours.objects.create(
            dayOfWeek=1, openingTime='08:00', closingTime='17:00', isClosed=False, isSpecialTime=False)
        self.url = reverse('opening-hours-retrieve-update-destroy',
                           kwargs={'pk': self.opening_hours.pk})

    def test_retrieve_opening_hours(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['dayOfWeek'], 1)

    def test_update_opening_hours(self):
        data = {'dayOfWeek': 2, 'openingTime': '09:00',
                'closingTime': '18:00', 'isClosed': False, 'isSpecialTime': False}
        response = self.client.put(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['dayOfWeek'], 2)

    def test_update_opening_hours_invalid_daysOfWeek(self):
        data = {'dayOfWeek': 10, 'openingTime': '09:00',
                'closingTime': '18:00', 'isClosed': False, 'isSpecialTime': False}
        response = self.client.put(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_opening_hours(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OpeningHours.objects.count(), 0)


class StoreListCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='tester', email='test@test.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

        self.store_data = {
            'name': 'Test Store',
            'address': [{
                'street': 'Test Street',
                'houseNumber': '123',
                'location': 'Test City',
                'postcode': '12345'
            }],
            'openingHours': [{
                'dayOfWeek': 1,
                'openingTime': '08:00',
                'closingTime': '17:00',
                'isClosed': False,
                'isSpecialTime': False
            }]
        }
        self.response = self.client.post(
            reverse('store-list-create'),
            data=self.store_data,
            format='json'
        )

    def test_create_store(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Store.objects.count(), 1)
        self.assertEqual(Store.objects.get().name, 'Test Store')

    def test_create_store_with_address(self):
        address = Address.objects.get()
        self.assertEqual(address.street, 'Test Street')
        self.assertEqual(address.houseNumber, '123')
        self.assertEqual(address.location, 'Test City')
        self.assertEqual(address.postcode, '12345')

    def test_create_store_with_opening_hours(self):
        opening_hours = OpeningHours.objects.get()
        self.assertEqual(opening_hours.dayOfWeek, 1)
        self.assertEqual(opening_hours.openingTime.strftime('%H:%M'), '08:00')
        self.assertEqual(opening_hours.closingTime.strftime('%H:%M'), '17:00')
        self.assertEqual(opening_hours.isClosed, False)
        self.assertEqual(opening_hours.isSpecialTime, False)

    def test_get_store_list(self):
        response = self.client.get(reverse('store-list-create'))
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StoreRetrieveUpdateDestroyViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='tester', email='test@test.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

        self.store = Store.objects.create(name='Test Store')
        self.address = Address.objects.create(
            street='Test Street', houseNumber='123', location='Test City', postcode='12345')
        self.opening_hours = OpeningHours.objects.create(
            dayOfWeek=1, openingTime='08:00', closingTime='17:00', isClosed=False, isSpecialTime=False)
        self.store.address.add(self.address)
        self.store.openingHours.add(self.opening_hours)
        self.store_data = {
            'name': 'Updated Test Store',
            'address': [{
                'street': 'Updated Test Street',
                'houseNumber': '123',
                'location': 'Updated Test City',
                'postcode': '12345'
            }],
            'openingHours': [{
                'dayOfWeek': 2,
                'openingTime': '09:00',
                'closingTime': '18:00',
                'isClosed': False,
                'isSpecialTime': False
            }]
        }
        self.response = self.client.put(
            reverse('store-retrieve-update-destroy',
                    kwargs={'pk': self.store.pk}),
            data=self.store_data,
            format='json'
        )

    def test_update_store(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(Store.objects.get().name, 'Updated Test Store')

    def test_update_store_invalid_address(self):
        self.store_data['address'][0]['street'] = 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
        self.store_data['name'] = 'New Test Store'
        self.store_data['openingHours'] = [{
            'dayOfWeek': 3,
            'openingTime': '10:00',
            'closingTime': '19:00',
            'isClosed': False,
            'isSpecialTime': False
        }]
        response = self.client.put(
            reverse('store-retrieve-update-destroy',
                    kwargs={'pk': self.store.pk}),
            data=self.store_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_store_invalid_opening_hours(self):
        self.store_data['openingHours'][0]['openingTime'] = '50:00'
        response = self.client.put(
            reverse('store-retrieve-update-destroy',
                    kwargs={'pk': self.store.pk}),
            data=self.store_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_store_missing_fields(self):
        self.store_data.pop('address')
        response = self.client.put(
            reverse('store-retrieve-update-destroy',
                    kwargs={'pk': self.store.pk}),
            data=self.store_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_store(self):
        response = self.client.get(
            reverse('store-retrieve-update-destroy', kwargs={'pk': self.store.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Test Store')

    def test_delete_store(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = self.client.delete(
            reverse('store-retrieve-update-destroy', kwargs={'pk': self.store.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
