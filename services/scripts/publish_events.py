import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from producer import ThreatEventProducer

producer = ThreatEventProducer()

for i in range(5):
    indicator = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    indicator_type = random.choice(["ip", "domain", "url", "hash"])
    related_technique = f"T{random.randint(1001, 9999)}"
    confidence = random.randint(50, 100)

    producer.publish_event(
        {
            "indicator": indicator,
            "indicator_type": indicator_type,
            "source": "test_script",
            "related_technique": related_technique,
            "confidence": confidence,
        }
    )
