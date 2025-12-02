from .sqs_queue import SQSQueue


class SNSTopic:
    """
    Mock SNS topic with:
    - Subscriber registry (SQS queues)
    - Broadcast to all subscribers
    """

    def __init__(self, name: str):
        self.name = name
        self._subscribers: list[SQSQueue] = []

    def subscribe(self, queue: SQSQueue):
        """Subscribe an SQS queue to this topic."""
        if queue not in self._subscribers:
            self._subscribers.append(queue)
            print(f"[SNS:{self.name}] Queue '{queue.name}' subscribed")

    def unsubscribe(self, queue: SQSQueue):
        """Unsubscribe an SQS queue from this topic."""
        if queue in self._subscribers:
            self._subscribers.remove(queue)
            print(f"[SNS:{self.name}] Queue '{queue.name}' unsubscribed")

    def publish(self, message: str) -> int:
        """
        Publish a message to all subscribers.
        Returns number of queues that received the message.
        """
        count = 0
        for queue in self._subscribers:
            queue.send_message(message)
            count += 1
        print(f"[SNS:{self.name}] Published to {count} subscriber(s)")
        return count

    def get_subscriber_count(self) -> int:
        return len(self._subscribers)
