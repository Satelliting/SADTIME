from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .views import HealthView


class APIRootView(APIView):
    """
    GET /api/
    Lists all available API sections.
    """

    def get(self, request):
        return Response(
            {
                "health": reverse("health", request=request),
                "threat_data": request.build_absolute_uri("/api/threat/"),
                "analytics": reverse("analytics-root", request=request),
                # "admin": request.build_absolute_uri("/admin/"),
            }
        )


urlpatterns = [
    path("", APIRootView.as_view(), name="api-root"),
    path("health/", HealthView.as_view(), name="health"),
]
