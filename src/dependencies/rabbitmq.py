import pika
import json


def publish_event(event: dict):

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='book_events', durable=True)

    message_body = json.dumps(event).encode('utf-8')

    channel.basic_publish(
        exchange='',
        routing_key='book_events',
        body=message_body,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    print(f"[FastAPI -> RabbitMQ] Отправлено событие: {event}")

    connection.close()