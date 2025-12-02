# Django API settings
API_BASE_URL = "http://127.0.0.1:8000"
EVENTS_ENDPOINT = f"{API_BASE_URL}/api/threat/events/"

# Queue/Topic names
TOPIC_NAME = "threat-events"
QUEUE_NAME = "threat-events-queue"
DLQ_NAME = "threat-events-dlq"

# Queue settings
VISIBILITY_TIMEOUT = 30  # seconds
MAX_RECEIVE_COUNT = 3  # retries before DLQ

# Consumer settings
POLL_INTERVAL = 2  # seconds between polls
BATCH_SIZE = 10  # messages per poll
