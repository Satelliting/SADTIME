import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from producer import ThreatEventProducer
from consumer import ThreatEventConsumer

producer = ThreatEventProducer()
consumer = ThreatEventConsumer(producer.get_queue())

print("=" * 50)
print("SADTIME Threat Event Consumer")
print("=" * 50)
print("Press Ctrl+C to stop\n")

consumer.start()
