from django.urls import path
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from .views import HealthView


class APIRootView(APIView):
    def get(self, request):
        return Response(
            {
                "health": reverse("health", request=request),
                "threat_data": request.build_absolute_uri("/api/threat/"),
                "analytics": reverse("analytics-root", request=request),
            }
        )


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {
                    "message": "Login successful",
                    "user": {
                        "username": user.username,
                        "is_staff": user.is_staff,
                    },
                }
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})


class MeView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {
                    "authenticated": True,
                    "user": {
                        "username": request.user.username,
                        "is_staff": request.user.is_staff,
                    },
                }
            )
        return Response({"authenticated": False})


urlpatterns = [
    path("", APIRootView.as_view(), name="api-root"),
    path("health/", HealthView.as_view(), name="health"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", MeView.as_view(), name="me"),
]
