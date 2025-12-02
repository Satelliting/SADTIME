import json
from datetime import datetime, timezone
from typing import Optional
from messageBroker import SNSTopic, SQSQueue, create_dlq
from config import (
    TOPIC_NAME,
    QUEUE_NAME,
    DLQ_NAME,
    VISIBILITY_TIMEOUT,
    MAX_RECEIVE_COUNT,
)


class ThreatEventProducer:
    """
    Publishes threat events to the messaging system.
    Sets up SNS topic with SQS subscriber on initialization.
    """

    _instance: Optional["ThreatEventProducer"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.dlq = create_dlq(DLQ_NAME)

        self.queue = SQSQueue(
            name=QUEUE_NAME,
            visibility_timeout=VISIBILITY_TIMEOUT,
            max_receive_count=MAX_RECEIVE_COUNT,
            dead_letter_queue=self.dlq,
        )

        self.topic = SNSTopic(TOPIC_NAME)
        self.topic.subscribe(self.queue)

        self._initialized = True
        print(f"[Producer] Initialized with topic '{TOPIC_NAME}'")

    def publish_event(self, event_data: dict) -> str:
        """
        Publish a threat event.

        Args:
            event_data: Dict with keys like indicator, indicator_type, source, etc.

        Returns:
            Message ID
        """
        if "timestamp" not in event_data:
            event_data["timestamp"] = datetime.now(timezone.utc).isoformat()

        message = json.dumps(event_data)
        self.topic.publish(message)
        return message

    def publish_batch(self, events: list[dict]) -> int:
        for event in events:
            self.publish_event(event)
        return len(events)

    def get_queue(self) -> SQSQueue:
        return self.queue

    def get_dlq(self) -> SQSQueue:
        return self.dlq
