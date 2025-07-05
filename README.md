# 🔄 Real-Time Kafka WebSocket Dashboard

🎥 [Watch the Demo Video](#) <!-- Add link after upload -->

A real-time data pipeline built using **FastAPI**, **WebSocket**, **Apache Kafka**, and **vanilla JavaScript**, with a live-updating browser UI. Messages sent from the frontend are streamed to Kafka via WebSocket, consumed in real-time, and displayed instantly in the UI.

---

## ✨ Features

- 🔌 **Send messages** via WebSocket from a browser
- 📡 **Produce Kafka events** from FastAPI backend
- 🧠 **Consume Kafka messages** inside FastAPI in real time
- 🖥️ **Live dashboard UI** using Server-Sent Events (SSE)
- 💡 Highlights messages from WebSocket vs Kafka
- 🧪 Built with simplicity, great for learning real-time data pipelines

---

## 📷 Demo Preview

<img src="preview.gif" width="700" alt="Live demo gif showing UI sending and receiving messages from Kafka">

> 🔔 Message sent ➝ WebSocket ➝ Kafka ➝ FastAPI ➝ SSE ➝ Frontend

---

## 🛠️ Tech Stack

| Layer       | Tech Used                         |
|-------------|-----------------------------------|
| Frontend    | HTML + JavaScript                 |
| Backend     | FastAPI + WebSocket + SSE         |
| Messaging   | Apache Kafka                      |
| Dev Tools   | Docker Compose (Kafka), Uvicorn   |

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/your-username/realtime-kafka-websocket-dashboard.git
cd realtime-kafka-websocket-dashboard
