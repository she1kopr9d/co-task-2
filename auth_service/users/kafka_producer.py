import confluent_kafka
import json
import logging


conf = {
    "bootstrap.servers": "kafka:9092",
}

producer = confluent_kafka.Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def send_user_registration_event(user_data: dict):
    topic = "user-registrations"
    message = json.dumps(user_data).encode("utf-8")
    producer.produce(topic, message, callback=delivery_report)
    producer.flush()
