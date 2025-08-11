from django.test import TestCase
from rest_framework.test import APITestCase


class AuthenticationFlowTests(APITestCase):
    """Ensure users can sign up and then log in."""

    def test_signup_and_login(self):
        signup_data = {
            "email": "alice@example.com",
            "password": "testpass123",
        }
        signup_response = self.client.post("/api/v1/users/signup/", signup_data)
        self.assertEqual(signup_response.status_code, 201)
        self.assertIn("token", signup_response.data)

        login_response = self.client.post(
            "/api/v1/users/login/", signup_data
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("token", login_response.data)


    def test_login_invalid_credentials(self):
        login_response = self.client.post(
            "/api/v1/users/login/",
            {"email": "nouser@example.com", "password": "wrong"},
        )
        self.assertEqual(login_response.status_code, 401)

    def test_signup_duplicate_email(self):
        data = {"email": "bob@example.com", "password": "pass123"}
        first = self.client.post("/api/v1/users/signup/", data)
        self.assertEqual(first.status_code, 201)
        second = self.client.post("/api/v1/users/signup/", data)
        self.assertEqual(second.status_code, 400)
        self.assertIn("error", second.data)


class UserSwipeTests(APITestCase):
    def setUp(self):
        signup_data = {"email": "carol@example.com", "password": "pass123"}
        res = self.client.post("/api/v1/users/signup/", signup_data)
        self.token = res.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_user_swipe_creates_favorite(self):
        response = self.client.post(
            "/api/v1/users/swipe/",
            {"restaurant": "Test Place", "liked": True},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["matched"])

        fav_response = self.client.get("/api/v1/favorites/")
        self.assertEqual(len(fav_response.data), 1)
        self.assertEqual(fav_response.data[0]["restaurant"], "Test Place")
