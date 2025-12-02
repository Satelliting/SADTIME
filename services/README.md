# SADTIME Services

Mock SNS/SQS messaging layer for local development.

- Three different terminals needed to run this setup.

## Running Django

```bash
cd backend
.venv\Scripts\activate # Windows
python manage.py runserver
```

## Running Consumer

```bash
cd services/scripts
python run_consumer.py
```

## Publishing Test Events

```bash
cd services/scripts
python publish_events.py
```
