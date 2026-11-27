import json
import threading
import pika
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI(title="Notification Service")


active_connections = []

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("[WS] Клиент подключился.")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"[WS] Клиент прислал: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("[WS] Клиент отключился.")


def rabbitmq_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='book_events', durable=True)
    print("[RabbitMQ] Ожидание сообщений в 'book_events'...")

    def callback(ch, method, properties, body):
        event = json.loads(body.decode('utf-8'))
        print(f"[RabbitMQ -> WS] Получено событие: {event}")

        notification = f"Новый заказ! Книга: {event.get('book_title')}, Пользователь: {event.get('user_id')}"

        for ws in active_connections:
            try:
                asyncio.run_coroutine_threadsafe(ws.send_text(notification), ws.loop)
            except Exception as e:
                print(f"Ошибка отправки: {e}")

    channel.basic_consume(queue='book_events', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=rabbitmq_consumer, daemon=True)
    thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)