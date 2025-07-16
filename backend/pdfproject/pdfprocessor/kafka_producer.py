from confluent_kafka import Producer
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

producer = Producer({
    'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
})

def delivery_report(err, msg):
    if err is not None:
        logger.error(f'Kafka delivery failed: {err}')
    else:
        logger.info(f'Kafka message delivered to {msg.topic()} [{msg.partion()}]')

def send_kafka_event(event, metadata=None):
    payload={
        'event': event,
        'metadata': metadata or {},
    }

    try:
        producer.produce(
            topic=settings.KAFKA_TOPIC,
            value=json.dumps(payload),
            callback=delivery_report
        )
        producer.poll(0)
    except Exception as e:
        logger.exception(f'Error sending Kafka event: {e}')