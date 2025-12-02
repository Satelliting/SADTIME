# 📘 **SADTIME**

### **Simulated ATT&CK-Driven Threat Intelligence Messaging Environment**

_A fully local, message‑driven threat‑intel pipeline._

---

# 🧭 Overview

**SADTIME** simulates a real-world threat intelligence ingestion and
analytics pipeline inspired by platforms.

It models how threat events flow through a distributed system:

- Threat data is **published** to a mock SNS-like topic
- Events are **queued** into a mock SQS inbox
- A **consumer** service processes, normalizes, and enriches events
- A **Django backend** stores the processed data
- A **React dashboard** displays analytics
- ATT&CK tactics & techniques drive classification

The entire environment runs **locally**, requires **no AWS**, and is
designed as a portfolio-quality demonstration of backend system design.

---

# 🔐 Threat Intelligence Scope

SADTIME includes a simplified cyber-threat model:

## **Threat Events**

Each event may include:

- `timestamp`
- `source` (e.g., "vendor feed", "internal SIEM")
- `indicator` (ip, domain, hash, url)
- `indicator_type`
- `related_technique` (ATT&CK Technique ID, e.g., T1059)
- `confidence`
- `metadata`

## **ATT&CK Data**

Static reference tables:

- Tactics (TAxxxx)
- Techniques (Txxxx)
- Sub-techniques (Txxxx.xx)
- Technique → Tactic mappings

## **Analytics Exposed**

The system provides:

- Indicators by type
- Techniques triggered over time
- Top threat sources
- Mapping events to techniques/tactics
- Queue depth & processing metrics

---

# 🚀 System Workflow

### **1. Producer publishes a threat event**

A Python script mimics a feed provider:

```python
sns.publish("threat_events", event_json)
```

### **2. SNS mock distributes the message**

SNS writes the event to each subscribed SQS queue.

### **3. SQS stores incoming messages**

The queue persists events in a file or SQLite table.

### **4. Consumer processes messages**

The worker simulates:

- JSON validation
- Indicator classification
- Technique enrichment
- Storing results in Django via API

### **5. Django exposes processed analytics**

REST endpoints include:

- `/api/indicators/counts`
- `/api/techniques/top`
- `/api/events/recent`

### **6. React dashboard displays insights**

A simple UI shows:

- Counts by indicator type
- Timeline charts
- Technique/tactic summaries

---

# 🛠 Technology Stack

### **Backend**

- Python 3.11+
- Django
- Django REST Framework
- SQLite (local)

### **Messaging Layer (Mock AWS)**

- SNS-like broadcaster
- SQS-like queue with visibility timeout
- Consumer worker with retry behavior

### **Frontend**

- React
- Vite

---

# 📡 Mock SNS/SQS Behavior

### **SNS Mock**

- Topic registry
- Subscribers list
- Broadcasts messages to queues

### **SQS Mock**

- FIFO message storage
- `visibility_timeout` semantics simulated
- Supports:
  - receive
  - delete
  - retry after failure

### **Consumer**

- Pulls messages
- Logs processing & errors
- Handles malformed messages
- Sends data to Django API

---

# 📊 Example Threat Event

```json
{
  "timestamp": "2025-01-19T04:16:00Z",
  "indicator": "185.244.25.10",
  "indicator_type": "ip",
  "source": "malware_feed",
  "related_technique": "T1059",
  "confidence": 82,
  "metadata": {
    "campaign": "ShadowHydra",
    "region": "US"
  }
}
```

---

# 🔍 Django API Preview

### **Events**

    GET /api/events/
    POST /api/events/

### **Indicators**

    GET /api/indicators/counts/

### **Techniques**

    GET /api/techniques/top/

---

# 📈 Dashboard Views

- **Event Stream View**
  Latest threat events from the backend.

- **Indicators Overview**
  Bar chart for IPs vs Domains vs Hashes.

- **ATT&CK Technique Heatmap**
  Count of events mapped to each technique.

---
