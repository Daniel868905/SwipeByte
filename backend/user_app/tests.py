from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from user_app.models import User



class AuthenticationFlowTests(APITestCase):
    """Ensure users can sign up, verify their email and then log in."""

    def _verify_user(self, email):
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return self.client.get(f"/api/v1/users/verify/{uid}/{token}/")

    def test_signup_and_login(self):
        signup_data = {
            "email": "alice@example.com",
            "password": "testpass123",
        }
        signup_response = self.client.post("/api/v1/users/signup/", signup_data)
        self.assertEqual(signup_response.status_code, 201)

        verify_response = self._verify_user("alice@example.com")
        self.assertEqual(verify_response.status_code, 200)


        login_response = self.client.post(
            "/api/v1/users/login/", signup_data
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("auth_token", login_response.cookies)


    def test_login_invalid_credentials(self):
        login_response = self.client.post(
            "/api/v1/users/login/",
            {"email": "nouser@example.com", "password": "wrong"},
        )
        self.assertEqual(login_response.status_code, 401)

    def test_signup_duplicate_email(self):
        data = {"email": "bob@example.com", "password": "pass12345"}
        first = self.client.post("/api/v1/users/signup/", data)
        self.assertEqual(first.status_code, 201)
        verify = self._verify_user("bob@example.com")
        self.assertEqual(verify.status_code, 200)
        second = self.client.post("/api/v1/users/signup/", data)
        self.assertEqual(second.status_code, 400)
        self.assertIn("error", second.data)


class UserSwipeTests(APITestCase):
    def setUp(self):
        signup_data = {"email": "carol@example.com", "password": "pass12345"}
        res = self.client.post("/api/v1/users/signup/", signup_data)
        verify = AuthenticationFlowTests._verify_user(self, "carol@example.com")
        self.assertEqual(verify.status_code, 200)
        login = self.client.post("/api/v1/users/login/", signup_data)
        self.assertEqual(login.status_code, 200)


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
