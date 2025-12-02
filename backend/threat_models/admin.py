from django.contrib import admin
from .models import *


@admin.register(ThreatEvent)
class ThreatEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "timestamp",
        "source",
        "raw_indicator",
        "indicator_type",
        "related_technique",
        "confidence",
        "metadata_json",
        "created_at",
    )
    list_filter = (
        "indicator_type",
        "related_technique",
        "confidence",
        "created_at",
    )
    search_fields = (
        "raw_indicator",
        "source",
        "metadata_json",
    )


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "value",
        "type",
        "first_seen",
        "last_seen",
        "event_count",
    )
    list_filter = (
        "type",
        "first_seen",
        "last_seen",
    )
    search_fields = (
        "value",
        "type",
    )


@admin.register(EventIndicatorMap)
class EventIndicatorMapAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event_id",
        "indicator_id",
    )


@admin.register(AttackTactic)
class AttackTacticAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")


@admin.register(AttackTechnique)
class AttackTechniqueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tactic_id")
    list_filter = ("tactic_id",)
    search_fields = ("id", "name")


@admin.register(TechniqueUsage)
class TechniqueUsageAdmin(admin.ModelAdmin):
    list_display = ("id", "event_id", "technique_id")
