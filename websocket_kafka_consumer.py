from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer
from kafka_producer import send_to_kafka  # External Kafka send logic
import threading
import asyncio
import json

# Create FastAPI app
app = FastAPI()

# Allow frontend to talk to backend without CORS issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (frontend HTML, etc.)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Async queue and event loop for pushing real-time updates to UI
loop = asyncio.get_event_loop()
messages = asyncio.Queue()

# ---------------- WebSocket Endpoint ----------------

# Frontend connects here via WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Get message from frontend WebSocket
            data = await websocket.receive_text()
            print(f"[WebSocket] Received: {data}")

            # Send it to Kafka
            send_to_kafka("realtime-topic", {"message": data})

            # Also push to SSE queue for frontend streaming
            await messages.put(f"[WebSocket] {data}")
        except Exception as e:
            print(f"WebSocket Error: {e}")
            break

# ---------------- Server-Sent Events (SSE) Endpoint ----------------

# Frontend connects here to receive Kafka/WebSocket messages in real-time
@app.get("/events")
async def sse_event_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            message = await messages.get()
            yield f"data: {message}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# ---------------- Kafka Consumer ----------------

# Background thread that listens to Kafka and streams messages to frontend
def start_kafka_consumer():
    consumer = KafkaConsumer(
        "realtime-topic",
        bootstrap_servers='localhost:9092',
        group_id='realtime-ui-group',
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    for msg in consumer:
        content = msg.value["message"]
        print(f"[Kafka Consumer] Received: {content}")
        asyncio.run_coroutine_threadsafe(
            messages.put(f"[Kafka] {content}"),
            loop
        )

# ---------------- Startup Hook ----------------

# Start the Kafka consumer thread when FastAPI boots up
@app.on_event("startup")
def startup_event():
    threading.Thread(target=start_kafka_consumer, daemon=True).start()
