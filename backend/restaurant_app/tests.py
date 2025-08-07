from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from unittest.mock import patch


class RestaurantSearchViewTests(TestCase):
    @patch('restaurant_app.views.requests.get')
    def test_search_returns_restaurants(self, mock_get):
        mock_get.return_value.json.return_value = {
            'results': [
                {
                    'place_id': '1',
                    'name': 'Test Restaurant',
                    'photos': [{'photo_reference': 'abc'}],
                    'rating': 4.5,
                    'price_level': 2,
                }
            ]
        }
        User = get_user_model()
        user = User.objects.create_user(username='test', email='test@example.com', password='pass1234')
        token = Token.objects.create(user=user)
        client = Client(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.get('/api/v1/restaurants/?distance=15&price=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Test Restaurant')
