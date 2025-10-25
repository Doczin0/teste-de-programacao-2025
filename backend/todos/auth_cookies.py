# todos/auth_cookies.py
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import logging

log = logging.getLogger("todos")
User = get_user_model()

COOKIE_ACCESS_NAME = "access_token"
COOKIE_REFRESH_NAME = "refresh_token"

def _cookie_kwargs():
    return {
        "httponly": True,
        "secure": not settings.DEBUG,
        "samesite": "Lax",
        "path": "/",
    }

def _find_username(identifier: str) -> str | None:
    if "@" in identifier:
        try:
            u = User.objects.get(email__iexact=identifier)
            return u.username
        except User.DoesNotExist:
            return None
    try:
        u = User.objects.get(username__iexact=identifier)
        return u.username
    except User.DoesNotExist:
        return None

@method_decorator(csrf_exempt, name="dispatch")
class CookieTokenObtainPairView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        identifier = (
            request.data.get("identifier")
            or request.data.get("username")
            or ""
        ).strip()
        password = (request.data.get("password") or "").strip()

        if not identifier or not password:
            return Response({"detail": "Informe usuário/e-mail e senha."}, status=400)

        username = _find_username(identifier)
        if not username:
            return Response({"detail": "Usuário/E-mail não encontrado."}, status=400)

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Credenciais inválidas."}, status=400)

        if not user.is_active:
            return Response({"detail": "Conta ainda não verificada."}, status=400)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        resp = Response({"detail": "Autenticado com sucesso."}, status=200)
        resp.set_cookie(COOKIE_ACCESS_NAME, access, **_cookie_kwargs())
        resp.set_cookie(COOKIE_REFRESH_NAME, str(refresh), **_cookie_kwargs())
        log.info("Login OK username=%s", username)
        return resp

@method_decorator(csrf_exempt, name="dispatch")
class CookieTokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.COOKIES.get(COOKIE_REFRESH_NAME)
        if not token:
            return Response({"detail": "Refresh ausente."}, status=401)
        try:
            refresh = RefreshToken(token)
            access = str(refresh.access_token)
        except Exception:
            resp = Response({"detail": "Refresh inválido/expirado."}, status=401)
            resp.delete_cookie(COOKIE_ACCESS_NAME, path="/")
            resp.delete_cookie(COOKIE_REFRESH_NAME, path="/")
            return resp
        resp = Response({"detail": "Token atualizado."}, status=200)
        resp.set_cookie(COOKIE_ACCESS_NAME, access, **_cookie_kwargs())
        resp.set_cookie(COOKIE_REFRESH_NAME, str(refresh), **_cookie_kwargs())
        return resp

@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        resp = Response({"detail": "Logout efetuado."}, status=200)
        resp.delete_cookie(COOKIE_ACCESS_NAME, path="/")
        resp.delete_cookie(COOKIE_REFRESH_NAME, path="/")
        return resp

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        u = request.user
        return Response({"id": u.id, "username": u.username, "email": u.email}, status=200)
