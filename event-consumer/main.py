from confluent_kafka import Consumer
from prometheus_client import Counter, start_http_server
import os
import json

KAFKA_BROKER = os.getenv("KAFKA_BROKER","kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC","pdf_events")

pdf_uploaded = Counter('pdf_uploaded_total', 'Number of PDFs uploaded')
pdf_downloaded = Counter('pdf_downloaded_total', 'Number of PDFs downloaded')

start_http_server(8001)

consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'metrics-consumer',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([KAFKA_TOPIC])

print("Kafka consumer started and listening...")

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Kafka error: {msg.error()}")
        continue

    try:
        event = json.loads(msg.value().decode('utf-8'))
        event_type = event.get('event')
        metadata = event.get('metadata',{})

        if event_type == 'pdf_uploaded':
            pdf_uploaded.inc()
            print("pdf_uploaded event processed")
        
        elif event_type == 'pdf_downloaded':
            pdf_downloaded.inc()
            print("pdf_downloaded event processed")
    
    except Exception as e:
        print(f"Failed to process event: {e}")