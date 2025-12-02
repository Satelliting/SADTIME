"""
Seed dynamic data: Indicators and ThreatEvents.
Can be run multiple times to add more test data.

Usage:
    python scripts/seed_events.py [--events N] [--indicators N]

Examples:
    python scripts/seed_events.py
    python scripts/seed_events.py --events 200 --indicators 100
"""

import os
import sys
import random
import argparse
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sadtime_backend.settings")

import django

django.setup()

from django.utils import timezone
from threat_models.models import (
    ThreatEvent,
    Indicator,
    EventIndicatorMap,
    AttackTechnique,
    TechniqueUsage,
)

# -----------------------------------------------------------------------------
# Sample data pools
# -----------------------------------------------------------------------------

SOURCES = [
    "malware_feed",
    "internal_siem",
    "honeypot",
    "threat_intel_platform",
    "osint_feed",
    "sandbox_analysis",
]

CAMPAIGNS = [
    "ShadowHydra",
    "DarkNexus",
    "PhantomBear",
    "CryptoWolf",
    "SilentViper",
    None,
]
REGIONS = ["US", "EU", "APAC", "LATAM", "MEA", None]
INDICATOR_TYPES = ["ip", "domain", "url", "hash"]


def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"


def random_domain():
    words = ["evil", "malware", "bad", "hack", "dark", "shadow", "crypto", "storm"]
    tlds = [".com", ".net", ".ru", ".cn", ".xyz", ".top"]
    return f"{random.choice(words)}{random.randint(1,999)}{random.choice(tlds)}"


def random_url():
    return f"http://{random_domain()}/{random.choice(['payload', 'download', 'update', 'config'])}.exe"


def random_hash():
    return "".join(random.choices("0123456789abcdef", k=64))


def random_indicator_value(indicator_type):
    generators = {
        "ip": random_ip,
        "domain": random_domain,
        "url": random_url,
        "hash": random_hash,
    }
    return generators[indicator_type]()


def random_datetime(days_back=90):
    """Random timezone-aware datetime within the last N days."""
    now = timezone.now()
    delta = timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    return now - delta


# -----------------------------------------------------------------------------
# Seed functions
# -----------------------------------------------------------------------------


def seed_indicators(count=50):
    print(f"Seeding {count} indicators...")
    created = 0
    for _ in range(count):
        ind_type = random.choice(INDICATOR_TYPES)
        value = random_indicator_value(ind_type)
        first_seen = random_datetime(days_back=90)
        last_seen = first_seen + timedelta(days=random.randint(0, 30))

        _, was_created = Indicator.objects.get_or_create(
            value=value,
            defaults={
                "type": ind_type,
                "first_seen": first_seen,
                "last_seen": last_seen,
                "event_count": random.randint(1, 100),
            },
        )
        if was_created:
            created += 1
    print(f"  Created {created} new indicators (total: {Indicator.objects.count()})")


def seed_events(count=100):
    print(f"Seeding {count} threat events...")
    techniques = list(AttackTechnique.objects.all())
    indicators = list(Indicator.objects.all())

    if not techniques:
        print("  WARNING: No techniques found. Run seed_reference_data.py first!")
    if not indicators:
        print(
            "  WARNING: No indicators found. Creating events without indicator links."
        )

    events_created = 0
    mappings_created = 0
    usages_created = 0

    for _ in range(count):
        ind_type = random.choice(INDICATOR_TYPES)
        technique = (
            random.choice(techniques) if techniques and random.random() > 0.2 else None
        )

        event = ThreatEvent.objects.create(
            timestamp=random_datetime(days_back=60),
            source=random.choice(SOURCES),
            raw_indicator=random_indicator_value(ind_type),
            indicator_type=ind_type,
            related_technique=technique.id if technique else None,
            confidence=random.randint(10, 100) if random.random() > 0.1 else None,
            metadata_json={
                "campaign": random.choice(CAMPAIGNS),
                "region": random.choice(REGIONS),
            },
        )
        events_created += 1

        # Link to 1-3 random indicators
        if indicators:
            linked = random.sample(
                indicators, k=min(random.randint(1, 3), len(indicators))
            )
            for ind in linked:
                _, was_created = EventIndicatorMap.objects.get_or_create(
                    event_id=event, indicator_id=ind
                )
                if was_created:
                    mappings_created += 1

        # Link to technique usage
        if technique:
            _, was_created = TechniqueUsage.objects.get_or_create(
                event_id=event, technique_id=technique
            )
            if was_created:
                usages_created += 1

    print(f"  Created {events_created} events (total: {ThreatEvent.objects.count()})")
    print(
        f"  Created {mappings_created} event-indicator mappings (total: {EventIndicatorMap.objects.count()})"
    )
    print(
        f"  Created {usages_created} technique usages (total: {TechniqueUsage.objects.count()})"
    )


def main():
    parser = argparse.ArgumentParser(description="Seed dynamic threat data")
    parser.add_argument(
        "--events", type=int, default=100, help="Number of events to create"
    )
    parser.add_argument(
        "--indicators", type=int, default=50, help="Number of indicators to create"
    )
    args = parser.parse_args()

    print("=" * 50)
    print("SADTIME Event/Indicator Seeder")
    print("=" * 50)
    seed_indicators(count=args.indicators)
    seed_events(count=args.events)
    print("=" * 50)
    print("Seeding complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
