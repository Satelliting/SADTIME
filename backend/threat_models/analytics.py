from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .models import *


class IndicatorCountsView(APIView):
    """
    GET /api/analytics/indicators/counts/
    Returns counts of indicators grouped by type.
    """

    def get(self, request):
        counts = (
            Indicator.objects.values("type")
            .annotate(count=Count("id"))
            .order_by("type")
        )
        return Response({"indicator_counts": list(counts)})


class TopTechniquesView(APIView):
    """
    GET /api/analytics/techniques/top/
    Returns most frequently used ATT&CK techniques.
    Optional query param: ?limit=10
    """

    def get(self, request):
        limit = int(request.query_params.get("limit", 10))

        top_techniques = (
            TechniqueUsage.objects.values("technique_id")
            .annotate(count=Count("id"))
            .order_by("-count")[:limit]
        )

        result = []
        for item in top_techniques:
            try:
                technique = AttackTechnique.objects.get(id=item["technique_id"])
                result.append(
                    {
                        "technique_id": item["technique_id"],
                        "name": technique.name,
                        "tactic_id": technique.tactic_id_id,
                        "count": item["count"],
                    }
                )
            except AttackTechnique.DoesNotExist:
                result.append(
                    {
                        "technique_id": item["technique_id"],
                        "name": "Unknown",
                        "count": item["count"],
                    }
                )

        return Response({"top_techniques": result})


class RecentEventsView(APIView):
    """
    GET /api/analytics/events/recent/
    Returns most recent threat events.
    Optional query params: ?limit=20&days=7
    """

    def get(self, request):
        limit = int(request.query_params.get("limit", 20))
        days = int(request.query_params.get("days", 7))

        cutoff = timezone.now() - timedelta(days=days)

        events = ThreatEvent.objects.filter(timestamp__gte=cutoff).order_by(
            "-timestamp"
        )[:limit]

        result = [
            {
                "id": e.id,
                "timestamp": e.timestamp,
                "source": e.source,
                "raw_indicator": e.raw_indicator,
                "indicator_type": e.indicator_type,
                "related_technique": e.related_technique,
                "confidence": e.confidence,
                "metadata": e.metadata_json,
            }
            for e in events
        ]

        return Response({"recent_events": result, "count": len(result)})


class EventTimelineView(APIView):
    """
    GET /api/analytics/events/timeline/
    Returns event counts grouped by day.
    Optional query param: ?days=30
    """

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        cutoff = timezone.now() - timedelta(days=days)

        events = (
            ThreatEvent.objects.filter(timestamp__gte=cutoff)
            .extra(select={"day": "date(timestamp)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        return Response({"timeline": list(events)})


class DashboardSummaryView(APIView):
    """
    GET /api/analytics/summary/
    Returns a quick overview for the dashboard.
    """

    def get(self, request):
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)

        return Response(
            {
                "total_events": ThreatEvent.objects.count(),
                "events_last_24h": ThreatEvent.objects.filter(
                    timestamp__gte=last_24h
                ).count(),
                "events_last_7d": ThreatEvent.objects.filter(
                    timestamp__gte=last_7d
                ).count(),
                "total_indicators": Indicator.objects.count(),
                "total_techniques_used": TechniqueUsage.objects.values("technique_id")
                .distinct()
                .count(),
            }
        )
