from typing import List
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
import asyncio
import asyncpg
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC")
PUBSUB_SUBSCRIPTION = os.getenv("PUBSUB_SUBSCRIPTION")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")


async def process_ids_async(ids: List[int]):
    # Connect to the database
    connection = await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST
    )

    # Publish data to Pub/Sub feed asynchronously
    publisher = pubsub_v1.PublisherClient.from_service_account_json(
        GOOGLE_APPLICATION_CREDENTIALS
    )
    topic_path = publisher.topic_path(GOOGLE_CLOUD_PROJECT, PUBSUB_TOPIC)

    # Query database for each ID and publish data to Pub/Sub feed
    for id in ids:
        # Query database asynchronously
        try:
            result = await connection.fetchrow(
                "SELECT * FROM ids_table WHERE id = $1", id
            )
            if result:  # Record exists, publish data
                data = str(result)
            else:  # Record doesn't exist, create it and publish
                # Insert logic
                await connection.execute("INSERT INTO ids_table (id) VALUES ($1)", id)
                # Assuming 'id' is the only column, adjust if needed
                print(f"Created record for ID {id}")

                # After creating, fetch the newly inserted data
                new_result = await connection.fetchrow(
                    "SELECT * FROM ids_table WHERE id = $1", id
                )
                data = str(new_result)

            # Get the message ID after publishing (fix await issue)
            future = publisher.publish(topic_path, data.encode())
            message_id = future.result()
            print(f"Published message ID: {message_id}")
        except Exception as e:
            print(f"Error publishing message for ID {id}: {e}")

    # Close database connection
    await connection.close()


# Function to listen to Pub/Sub feed
async def listen_to_pubsub():
    subscriber = pubsub_v1.SubscriberClient.from_service_account_json(
        GOOGLE_APPLICATION_CREDENTIALS
    )
    subscription_path = subscriber.subscription_path(
        GOOGLE_CLOUD_PROJECT, PUBSUB_SUBSCRIPTION
    )

    def callback(message):
        # Process received message
        data = message.data.decode("utf-8")
        print(f"Received message: {data}")

        # Acknowledge the message
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # Keep the main thread running to continue listening for messages
    await asyncio.Event().wait()


# Run Pub/Sub listener in a separate thread
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(listen_to_pubsub())
    yield


app = FastAPI(lifespan=lifespan)


# Endpoint to submit IDs for processing
@app.post("/process-ids/")
async def process_ids(background_tasks: BackgroundTasks, ids: List[int]):
    # Process IDs asynchronously in the background
    background_tasks.add_task(process_ids_async, ids)
    return {"message": "IDs submitted for processing"}


@app.get("/")
def read_root():
    return {"Hello,": "Welcome to FastAPI!"}
