from .sqs_queue import SQSQueue


def create_dlq(name: str = "threat-events-dlq") -> SQSQueue:
    """
    Create a dead letter queue.
    DLQs have no DLQ of their own and higher visibility timeout.
    """
    return SQSQueue(
        name=name,
        visibility_timeout=300,  # 5 minutes
        max_receive_count=999,  # Effectively no limit
        dead_letter_queue=None,
    )
