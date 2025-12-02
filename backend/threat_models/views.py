from rest_framework import viewsets
from .models import *
from .serializers import *


class AttackTacticViewSet(viewsets.ModelViewSet):
    queryset = AttackTactic.objects.all()
    serializer_class = AttackTacticSerializer


class AttackTechniqueViewSet(viewsets.ModelViewSet):
    queryset = AttackTechnique.objects.all()
    serializer_class = AttackTechniqueSerializer


class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


class ThreatEventViewSet(viewsets.ModelViewSet):
    queryset = ThreatEvent.objects.all()
    serializer_class = ThreatEventSerializer


class EventIndicatorMapViewSet(viewsets.ModelViewSet):
    queryset = EventIndicatorMap.objects.all()
    serializer_class = EventIndicatorMapSerializer


class TechniqueUsageViewSet(viewsets.ModelViewSet):
    queryset = TechniqueUsage.objects.all()
    serializer_class = TechniqueUsageSerializer
