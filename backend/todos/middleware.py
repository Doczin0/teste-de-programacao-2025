# todos/middleware.py
import base64
import json
import logging

from django.utils.deprecation import MiddlewareMixin

from .auth_cookies import COOKIE_ACCESS_NAME, COOKIE_REFRESH_NAME

log = logging.getLogger(__name__)


def _extract_payload(token: str) -> dict | None:
    """Best-effort decode of the JWT payload without validating signature."""
    parts = token.split(".")
    if len(parts) != 3:
        return None

    payload_segment = parts[1]
    padding = "=" * (-len(payload_segment) % 4)

    try:
        decoded = base64.urlsafe_b64decode(payload_segment + padding)
        return json.loads(decoded.decode("utf-8"))
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return None


class CookieToAuthorizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if "HTTP_AUTHORIZATION" in request.META:
            return

        token = request.COOKIES.get(COOKIE_ACCESS_NAME)
        if not token:
            return

        payload = _extract_payload(token)
        if not payload or payload.get("token_type") != "access":
            log.info("Invalid access token cookie detected; scheduling cleanup.")
            request._invalid_auth_cookies = True
            return

        request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    def process_response(self, request, response):
        if getattr(request, "_invalid_auth_cookies", False):
            response.delete_cookie(COOKIE_ACCESS_NAME, path="/")
            response.delete_cookie(COOKIE_REFRESH_NAME, path="/")
        return response
