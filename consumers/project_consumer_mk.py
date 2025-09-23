"""
project_consumer_moses.py

Consume json messages from a Kafka topic and visualize sentiment trend in real-time.

JSON is a set of key:value pairs. 

Example serialized Kafka message
"{\"message\": \"I love Python!\", \"author\": \"Eve\", \"sentiment\": 0.9, \"timestamp\": \"2025-01-29 14:35:20\"}"

Example JSON message (after deserialization) to be analyzed
{"message": "I love Python!", "author": "Eve", "sentiment": 0.9, "timestamp": "2025-01-29 14:35:20"}
"""

#####################################
# Import Modules
#####################################

# Import packages from Python Standard Library
import os
import json  # handle JSON parsing

# Import external packages
from dotenv import load_dotenv

# IMPORTANT - Visualization
# Use TkAgg backend to ensure matplotlib can open a GUI window properly on macOS
import matplotlib
matplotlib.use("TkAgg")

# Import Matplotlib.pyplot for live plotting
# Use the common alias 'plt' for Matplotlib.pyplot
# Know pyplot well
import matplotlib.pyplot as plt

# Import functions from local modules
from utils.utils_consumer import create_kafka_consumer
from utils.utils_logger import logger

#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################


def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("PROJECT_TOPIC", "project_json")
    logger.info(f"Kafka topic: {topic}")
    return topic


def get_kafka_consumer_group_id() -> str:
    """Fetch Kafka consumer group id from environment or use default."""
    group_id: str = os.getenv("PROJECT_CONSUMER_GROUP_ID", "project_group")
    logger.info(f"Kafka consumer group id: {group_id}")
    return group_id


#####################################
# Set up data structures
#####################################

# Initialize lists to track time and sentiment
# These will grow as new messages arrive
timestamps = []
sentiments = []

#####################################
# Set up live visuals
#####################################

# Use the subplots() method to create a tuple containing
# two objects at once:
# - a figure (which can have many axis)
# - an axis (what they call a chart in Matplotlib)
fig, ax = plt.subplots()

# Use the ion() method (stands for "interactive on")
# to turn on interactive mode for live updates
plt.ion()

#####################################
# Define an update chart function for live plotting
# This will get called every time a new message is processed
#####################################


def update_chart():
    """Update the live chart with the latest sentiment trend."""
    # Clear the previous chart so new data can be plotted
    ax.clear()

    # Plot sentiment values over time
    ax.plot(timestamps, sentiments, color="green", marker="o", linestyle="-")

    # Use the built-in axes methods to set the labels and title
    ax.set_xlabel("Time")
    ax.set_ylabel("Sentiment Score")
    ax.set_title("Real-Time Sentiment Trend - Moses")

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha="right")

    # Use the tight_layout() method to automatically adjust the padding
    plt.tight_layout()

    # Draw the chart
    plt.draw()

    # Pause briefly to allow some time for the chart to render
    plt.pause(0.01)


#####################################
# Function to process a single message
#####################################


def process_message(message: str) -> None:
    """
    Process a single JSON message from Kafka and update the chart.

    Args:
        message (str): The JSON message as a string.
    """
    try:
        # Log the raw message for debugging
        logger.debug(f"Raw message: {message}")

        # Parse the JSON string into a Python dictionary
        message_dict: dict = json.loads(message)

        # Ensure the processed JSON is logged for debugging
        logger.info(f"Processed JSON message: {message_dict}")

        # Ensure it's a dictionary before accessing fields
        if isinstance(message_dict, dict):
            # Extract the 'timestamp' and 'sentiment' fields
            timestamp = message_dict.get("timestamp")
            sentiment = message_dict.get("sentiment")

            if timestamp and sentiment is not None:
                # Append new data to the lists
                timestamps.append(timestamp)
                sentiments.append(sentiment)

                # Log what was appended
                logger.info(f"Appended timestamp={timestamp}, sentiment={sentiment}")

                # Update the chart
                update_chart()

                # Log the updated chart status
                logger.info(f"Chart updated successfully for message: {message}")
        else:
            logger.error(f"Expected a dictionary but got: {type(message_dict)}")

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON message: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


#####################################
# Define main function for this module
#####################################


def main() -> None:
    """
    Main entry point for the consumer.

    - Reads the Kafka topic name and consumer group ID from environment variables.
    - Creates a Kafka consumer using the `create_kafka_consumer` utility.
    - Polls messages and updates a live chart.
    """
    logger.info("START consumer.")

    # fetch .env content
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()
    logger.info(f"Consumer: Topic '{topic}' and group '{group_id}'...")

    # Create the Kafka consumer using the helpful utility function.
    consumer = create_kafka_consumer(topic, group_id)

    # Poll and process messages
    logger.info(f"Polling messages from topic '{topic}'...")
    try:
        for message in consumer:
            # message is a complex object with metadata and value
            # Use the value attribute to extract the message as a string
            message_str = message.value
            logger.debug(f"Received message at offset {message.offset}: {message_str}")
            process_message(message_str)
    except KeyboardInterrupt:
        # Handle CTRL+C gracefully
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Error while consuming messages: {e}")
    finally:
        # Always close the consumer on exit
        consumer.close()
        logger.info(f"Kafka consumer for topic '{topic}' closed.")

    logger.info(f"END consumer for topic '{topic}' and group '{group_id}'.")


#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":

    # Call the main function to start the consumer
    main()

    # Turn off interactive mode after completion
    plt.ioff()

    # Display the final chart
    plt.show()
