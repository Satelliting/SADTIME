import time
import threading
import uuid
import sqlite3
from typing import Optional
from pathlib import Path


DEFAULT_DB_PATH = Path(__file__).parent.parent / "queue.db"


class SQSQueue:
    """
    Mock SQS queue backed by SQLite for cross-process persistence.
    """

    def __init__(
        self,
        name: str,
        visibility_timeout: int = 30,
        max_receive_count: int = 3,
        dead_letter_queue: Optional["SQSQueue"] = None,
        db_path: Path = DEFAULT_DB_PATH,
    ):
        self.name = name
        self.visibility_timeout = visibility_timeout
        self.max_receive_count = max_receive_count
        self.dead_letter_queue = dead_letter_queue
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        """Create tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    queue_name TEXT NOT NULL,
                    body TEXT NOT NULL,
                    receive_count INTEGER DEFAULT 0,
                    visible_after REAL DEFAULT 0,
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_queue_visible ON messages (queue_name, visible_after)"
            )

    def send_message(self, body: str) -> str:
        """Add a message to the queue."""
        msg_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO messages (id, queue_name, body) VALUES (?, ?, ?)",
                (msg_id, self.name, body),
            )
        return msg_id

    def receive_message(self, max_messages: int = 1) -> list[dict]:
        """Receive messages, marking them invisible."""
        now = time.time()
        received = []

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            # Get visible messages
            rows = conn.execute(
                """
                SELECT id, body, receive_count 
                FROM messages 
                WHERE queue_name = ? AND visible_after <= ?
                ORDER BY created_at
                LIMIT ?
            """,
                (self.name, now, max_messages),
            ).fetchall()

            for row in rows:
                new_receive_count = row["receive_count"] + 1
                receipt_handle = str(uuid.uuid4())
                visible_after = now + self.visibility_timeout

                # Check if max retries exceeded
                if new_receive_count > self.max_receive_count:
                    # Move to DLQ
                    if self.dead_letter_queue:
                        self.dead_letter_queue.send_message(row["body"])
                        print(f"[SQS:{self.name}] Message {row['id']} moved to DLQ")
                    conn.execute("DELETE FROM messages WHERE id = ?", (row["id"],))
                    continue

                # Update visibility and receive count
                conn.execute(
                    """
                    UPDATE messages 
                    SET visible_after = ?, receive_count = ?
                    WHERE id = ?
                """,
                    (visible_after, new_receive_count, row["id"]),
                )

                received.append(
                    {
                        "MessageId": row["id"],
                        "Body": row["body"],
                        "ReceiptHandle": row["id"],  # Use message ID as receipt handle
                        "ApproximateReceiveCount": new_receive_count,
                    }
                )

        return received

    def delete_message(self, receipt_handle: str) -> bool:
        """Delete a message after successful processing."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM messages WHERE id = ? AND queue_name = ?",
                (receipt_handle, self.name),
            )
            return cursor.rowcount > 0

    def get_queue_size(self) -> dict:
        """Return queue statistics."""
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            visible = conn.execute(
                "SELECT COUNT(*) FROM messages WHERE queue_name = ? AND visible_after <= ?",
                (self.name, now),
            ).fetchone()[0]
            in_flight = conn.execute(
                "SELECT COUNT(*) FROM messages WHERE queue_name = ? AND visible_after > ?",
                (self.name, now),
            ).fetchone()[0]
        return {
            "visible": visible,
            "in_flight": in_flight,
            "total": visible + in_flight,
        }

    def purge(self):
        """Clear all messages from the queue."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM messages WHERE queue_name = ?", (self.name,))
