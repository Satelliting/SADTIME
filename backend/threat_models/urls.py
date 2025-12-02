from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"events", ThreatEventViewSet)
router.register(r"indicators", IndicatorViewSet)
router.register(r"event-indicator-map", EventIndicatorMapViewSet)
router.register(r"tactics", AttackTacticViewSet)
router.register(r"techniques", AttackTechniqueViewSet)
router.register(r"technique-usage", TechniqueUsageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
