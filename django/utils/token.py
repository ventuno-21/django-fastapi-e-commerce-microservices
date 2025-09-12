import jwt
from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed
from types import SimpleNamespace
from .logger import logger
from django.conf import settings


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")


class JWTAuthentication(authentication.BaseAuthentication):
    """
    DRF authentication backend that validates a JWT issued by the FastAPI Auth service.
    It DOES NOT create a local Django user record. Instead it returns a lightweight
    user-like object with `.is_authenticated` True and `.id` set to the user id from token.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid payload")

        # Now in views.py we have an access to request.user.is_authenticated/id/username/email
        user = SimpleNamespace(
            is_authenticated=True,
            id=int(user_id),
            username=payload.get("username"),
            email=payload.get("email"),
        )

        logger.info(user.is_authenticated)
        logger.debug(user.id)

        return (user, None)
