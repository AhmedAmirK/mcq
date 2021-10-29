from kafka import KafkaProducer
from django.conf import settings
import json

TOPIC = 'exam_submit'


producer = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER,
                         value_serializer=lambda d: json.dumps(d).encode('utf-8'))



def publish_message(data):
    producer.send(TOPIC, data)
    producer.flush()