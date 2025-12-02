"""
Seed reference data: ATT&CK Tactics and Techniques.
Run once to populate static lookup tables.

Usage:
    python scripts/seed_reference_data.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sadtime_backend.settings")

import django

django.setup()

from threat_models.models import AttackTactic, AttackTechnique

TACTICS = [
    ("TA0001", "Initial Access", "Techniques to gain initial foothold"),
    ("TA0002", "Execution", "Techniques to run malicious code"),
    ("TA0003", "Persistence", "Techniques to maintain access"),
    ("TA0004", "Privilege Escalation", "Techniques to gain higher permissions"),
    ("TA0005", "Defense Evasion", "Techniques to avoid detection"),
    ("TA0006", "Credential Access", "Techniques to steal credentials"),
    ("TA0007", "Discovery", "Techniques to explore the environment"),
    ("TA0008", "Lateral Movement", "Techniques to move through network"),
    ("TA0009", "Collection", "Techniques to gather target data"),
    ("TA0010", "Exfiltration", "Techniques to steal data"),
    ("TA0011", "Command and Control", "Techniques for C2 communication"),
]

TECHNIQUES = [
    ("T1059", "Command and Scripting Interpreter", "TA0002"),
    ("T1059.001", "PowerShell", "TA0002"),
    ("T1059.003", "Windows Command Shell", "TA0002"),
    ("T1566", "Phishing", "TA0001"),
    ("T1566.001", "Spearphishing Attachment", "TA0001"),
    ("T1566.002", "Spearphishing Link", "TA0001"),
    ("T1078", "Valid Accounts", "TA0001"),
    ("T1053", "Scheduled Task/Job", "TA0003"),
    ("T1547", "Boot or Logon Autostart Execution", "TA0003"),
    ("T1548", "Abuse Elevation Control Mechanism", "TA0004"),
    ("T1070", "Indicator Removal", "TA0005"),
    ("T1055", "Process Injection", "TA0005"),
    ("T1003", "OS Credential Dumping", "TA0006"),
    ("T1018", "Remote System Discovery", "TA0007"),
    ("T1021", "Remote Services", "TA0008"),
    ("T1105", "Ingress Tool Transfer", "TA0011"),
    ("T1071", "Application Layer Protocol", "TA0011"),
]


def seed_tactics():
    print("Seeding tactics...")
    created = 0
    for tactic_id, name, desc in TACTICS:
        _, was_created = AttackTactic.objects.get_or_create(
            id=tactic_id,
            defaults={"name": name, "description": desc},
        )
        if was_created:
            created += 1
    print(f"  Created {created} new tactics (total: {AttackTactic.objects.count()})")


def seed_techniques():
    print("Seeding techniques...")
    created = 0
    for tech_id, name, tactic_id in TECHNIQUES:
        tactic = AttackTactic.objects.get(id=tactic_id)
        _, was_created = AttackTechnique.objects.get_or_create(
            id=tech_id,
            defaults={
                "name": name,
                "description": f"Description for {name}",
                "tactic_id": tactic,
            },
        )
        if was_created:
            created += 1
    print(
        f"  Created {created} new techniques (total: {AttackTechnique.objects.count()})"
    )


def main():
    print("=" * 50)
    print("SADTIME Reference Data Seeder")
    print("=" * 50)
    seed_tactics()
    seed_techniques()
    print("=" * 50)
    print("Reference data seeding complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
