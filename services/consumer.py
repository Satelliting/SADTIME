import json
import time
import requests
from messageBroker import SQSQueue
from config import EVENTS_ENDPOINT, POLL_INTERVAL, BATCH_SIZE


class ThreatEventConsumer:
    """
    Consumes threat events from SQS and posts to Django API.
    """

    def __init__(
        self,
        queue: SQSQueue,
        api_endpoint: str = EVENTS_ENDPOINT,
        poll_interval: float = POLL_INTERVAL,
        batch_size: int = BATCH_SIZE,
    ):
        self.queue = queue
        self.api_endpoint = api_endpoint
        self.poll_interval = poll_interval
        self.batch_size = batch_size
        self._running = False

        # Stats
        self.processed_count = 0
        self.failed_count = 0

    def process_message(self, message: dict) -> bool:
        """
        Process a single message.

        Returns:
            True if successful, False if failed
        """
        try:
            body = json.loads(message["Body"])

            payload = {
                "timestamp": body.get("timestamp"),
                "source": body.get("source", "unknown"),
                "raw_indicator": body.get("indicator"),
                "indicator_type": body.get("indicator_type"),
                "related_technique": body.get("related_technique"),
                "confidence": body.get("confidence"),
                "metadata_json": body.get("metadata", {}),
            }

            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            if response.status_code in (200, 201):
                print(f"[Consumer] Created event: {payload['raw_indicator']}")
                return True
            else:
                print(
                    f"[Consumer] API error {response.status_code}: {response.text[:100]}"
                )
                return False

        except json.JSONDecodeError as e:
            print(f"[Consumer] Invalid JSON: {e}")
            return False
        except requests.RequestException as e:
            print(f"[Consumer] Request failed: {e}")
            return False
        except Exception as e:
            print(f"[Consumer] Unexpected error: {e}")
            return False

    def process_batch(self) -> dict:
        """
        Process one batch of messages.

        Returns:
            Dict with processed/failed counts
        """
        messages = self.queue.receive_message(max_messages=self.batch_size)

        if not messages:
            return {"processed": 0, "failed": 0}

        processed = 0
        failed = 0

        for msg in messages:
            success = self.process_message(msg)

            if success:
                self.queue.delete_message(msg["ReceiptHandle"])
                processed += 1
                self.processed_count += 1
            else:
                failed += 1
                self.failed_count += 1

        return {"processed": processed, "failed": failed}

    def start(self):
        """
        Start the consumer loop. Blocks forever.
        Use Ctrl+C to stop.
        """
        self._running = True
        print(f"[Consumer] Starting... polling every {self.poll_interval}s")
        print(f"[Consumer] Posting to: {self.api_endpoint}")

        try:
            while self._running:
                result = self.process_batch()

                if result["processed"] or result["failed"]:
                    print(
                        f"[Consumer] Batch: {result['processed']} ok, {result['failed']} failed"
                    )

                time.sleep(self.poll_interval)

        except KeyboardInterrupt:
            print(
                f"\n[Consumer] Stopped. Total: {self.processed_count} processed, {self.failed_count} failed"
            )
            self._running = False

    def stop(self):
        self._running = False

    def get_stats(self) -> dict:
        return {
            "processed": self.processed_count,
            "failed": self.failed_count,
            "queue_size": self.queue.get_queue_size(),
        }
