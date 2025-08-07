from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from unittest.mock import patch, Mock


class RestaurantSearchViewTests(TestCase):
    @patch("restaurant_app.views.requests.get")
    def test_search_includes_fast_food_when_price_one(self, mock_get):
        def mock_response(data):
            m = Mock()
            m.json.return_value = data
            return m

        mock_get.side_effect = [
            mock_response(
                {
                    "results": [
                        {
                            "place_id": "1",
                            "name": "Test Restaurant",
                            "photos": [{"photo_reference": "abc"}],
                            "rating": 4.5,
                            "price_level": 2,
                        }
                    ]
                }
            ),
            mock_response(
                {
                    "results": [
                        {
                            "place_id": "2",
                            "name": "Test Fast Food",
                            "photos": [],
                            "rating": 3.5,
                            "price_level": 1,
                        }
                    ]
                }
            ),
        ]
        User = get_user_model()
        user = User.objects.create_user(
            username="test", email="test@example.com", password="pass1234"
        )
        token = Token.objects.create(user=user)
        client = Client(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = client.get(
            "/api/v1/restaurants/?distance=15&price=1&lat=1&lon=2"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        names = {r["name"] for r in data}
        self.assertIn("Test Restaurant", names)
        self.assertIn("Test Fast Food", names)
        self.assertEqual(mock_get.call_count, 2)
