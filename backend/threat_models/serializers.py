from rest_framework import serializers
from .models import *


class AttackTacticSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttackTactic
        fields = "__all__"


class AttackTechniqueSerializer(serializers.ModelSerializer):
    tactic = AttackTacticSerializer(source="tactic_id", read_only=True)

    class Meta:
        model = AttackTechnique
        fields = ["id", "name", "description", "tactic_id", "tactic"]


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = "__all__"


class ThreatEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatEvent
        fields = "__all__"


class EventIndicatorMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventIndicatorMap
        fields = "__all__"


class TechniqueUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueUsage
        fields = "__all__"
