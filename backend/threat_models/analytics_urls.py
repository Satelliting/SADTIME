from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .analytics import (
    IndicatorCountsView,
    TopTechniquesView,
    RecentEventsView,
    EventTimelineView,
    DashboardSummaryView,
)


class AnalyticsRootView(APIView):
    """
    GET /api/analytics/
    Lists all available analytics endpoints.
    """

    def get(self, request):
        return Response(
            {
                "summary": reverse("dashboard-summary", request=request),
                "indicators_counts": reverse("indicator-counts", request=request),
                "techniques_top": reverse("top-techniques", request=request),
                "events_recent": reverse("recent-events", request=request),
                "events_timeline": reverse("event-timeline", request=request),
            }
        )


urlpatterns = [
    path("", AnalyticsRootView.as_view(), name="analytics-root"),
    path("indicators/counts/", IndicatorCountsView.as_view(), name="indicator-counts"),
    path("techniques/top/", TopTechniquesView.as_view(), name="top-techniques"),
    path("events/recent/", RecentEventsView.as_view(), name="recent-events"),
    path("events/timeline/", EventTimelineView.as_view(), name="event-timeline"),
    path("summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
]
