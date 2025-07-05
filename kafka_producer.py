# Import KafkaProducer from the kafka-python library
from kafka import KafkaProducer

# Import json for serializing Python objects to JSON strings
import json

# Initialize a KafkaProducer instance
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Kafka broker location
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Convert Python dict to JSON and encode as UTF-8 bytes
)

# Function to send a message to a specific Kafka topic
def send_to_kafka(topic, message):
    """
    Sends a JSON-encoded message to the given Kafka topic.
    
    Args:
        topic (str): The Kafka topic to send the message to.
        message (dict): The message data (Python dict) to send.
    """
    producer.send(topic, message)  # Send message asynchronously
    producer.flush()               # Ensure the message is actually sent (force push from buffer)
