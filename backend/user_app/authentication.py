from rest_framework.authentication import TokenAuthentication


class CookieTokenAuthentication(TokenAuthentication):
    """Authenticate using a token stored in an ``auth_token`` cookie."""

    def authenticate(self, request):
        token = request.COOKIES.get('auth_token')
        if not token:
            return None
        return self.authenticate_credentials(token)