from rest_framework.authentication import TokenAuthentication


class CookieTokenAuthentication(TokenAuthentication):
    """Authenticate using a token stored in an ``auth_token`` cookie.

    If no such cookie is present, fall back to the standard
    ``TokenAuthentication`` behavior which looks for the token in the
    ``Authorization`` header.  This allows clients to authenticate using
    either approach.
    """

    def authenticate(self, request):
        token = request.COOKIES.get('auth_token')
        if token:
            return self.authenticate_credentials(token)
        return super().authenticate(request)