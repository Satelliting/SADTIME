from django.db import models


class ThreatEvent(models.Model):
    timestamp = models.DateTimeField()  # When the event occurred
    source = models.CharField(
        max_length=255
    )  # Origin of the event (e.g., malware feed, internal SIEM)
    raw_indicator = models.CharField(
        max_length=255
    )  # The original indicator value (IP, domain, URL, hash)
    indicator_type = models.CharField(
        max_length=50
    )  # Type of the indicator (ip, domain, url, hash)
    related_technique = models.CharField(
        max_length=20, null=True, blank=True
    )  # Optional ATT&CK technique ID (e.g., T1059)
    confidence = models.IntegerField(
        null=True, blank=True
    )  # Optional score representing trust in the event
    metadata_json = models.JSONField(
        default=dict
    )  # Any extra info, like campaign name, region, etc.
    created_at = models.DateTimeField(auto_now_add=True)  # When the event was recorded


class Indicator(models.Model):
    value = models.CharField(
        max_length=255
    )  # The actual indicator (185.244.25.10, malicious.com)
    type = models.CharField(max_length=50)  # Type of indicator (ip, domain, url, hash)
    first_seen = models.DateTimeField(
        auto_now_add=True
    )  # When this indicator first appeared
    last_seen = models.DateTimeField(auto_now=True)  # When this indicator was last seen
    event_count = models.IntegerField(
        null=True, blank=True
    )  # How many events reference this indicator


class EventIndicatorMap(models.Model):
    event_id = models.ForeignKey(
        "ThreatEvent", on_delete=models.CASCADE
    )  # Links to ThreatEvent
    indicator_id = models.ForeignKey(
        "Indicator", on_delete=models.CASCADE
    )  # Links to Indicator


class AttackTechnique(models.Model):
    id = models.CharField(max_length=255, primary_key=True)  # Technique ID (Txxxx)
    name = models.CharField(
        max_length=255
    )  # Technique name (“Command and Scripting Interpreter”)
    description = models.TextField()  # Description of the technique
    tactic_id = models.ForeignKey("AttackTactic", on_delete=models.CASCADE)


class AttackTactic(models.Model):
    id = models.CharField(max_length=255, primary_key=True)  # Tactic ID (TAxxxx)
    name = models.CharField(
        max_length=255
    )  # Tactic name ("Command and Scripting Interpreter")
    description = models.TextField()  # Description of the tactic


class TechniqueUsage(models.Model):
    event_id = models.ForeignKey("ThreatEvent", on_delete=models.CASCADE)
    technique_id = models.ForeignKey("AttackTechnique", on_delete=models.CASCADE)
