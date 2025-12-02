import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from messageBroker import SNSTopic, SQSQueue, create_dlq


def main():
    print("=" * 50)
    print("SNS/SQS Message Broker")
    print("=" * 50)

    dlq = create_dlq("threat-events-dlq")

    main_queue = SQSQueue(
        name="threat-events-queue",
        visibility_timeout=10,
        max_receive_count=3,
        dead_letter_queue=dlq,
    )

    topic = SNSTopic("threat-events")
    topic.subscribe(main_queue)

    # Publish some test events
    print("\n--- Publishing events ---")
    for i in range(3):
        event = {
            "timestamp": "2025-01-19T04:16:00Z",
            "indicator": f"192.168.1.{i+1}",
            "indicator_type": "ip",
            "source": "demo_feed",
            "related_technique": "T1059",
            "confidence": 80 + i,
        }
        topic.publish(json.dumps(event))

    print("\n--- Receiving messages ---")
    print(f"Queue size: {main_queue.get_queue_size()}")

    messages = main_queue.receive_message(max_messages=10)
    for msg in messages:
        print(f"\nReceived: {msg['MessageId']}")
        body = json.loads(msg["Body"])
        print(f"  Indicator: {body['indicator']}")
        print(f"  Receive count: {msg['ApproximateReceiveCount']}")

        main_queue.delete_message(msg["ReceiptHandle"])

    print(f"\nFinal queue size: {main_queue.get_queue_size()}")
    print(f"DLQ size: {dlq.get_queue_size()}")


if __name__ == "__main__":
    main()
