# Buzzline Project – Real-Time JSON Consumer (Moses)

This project demonstrates **real-time data streaming with Kafka** and Python.  
It includes a **custom producer** that generates JSON messages and a **consumer** that processes those messages to create **live visualizations of sentiment trends**.

---

## Features
- **Producer**: Streams random JSON messages containing:
  - message text  
  - author  
  - timestamp  
  - category  
  - sentiment score (stubbed for now)  
  - keyword mentioned  
  - message length  

- **Consumer (Custom: `project_consumer_mk.py`)**:
  - Reads messages from Kafka topic `project_json` (from `.env`).  
  - Extracts only the fields needed (`timestamp`, `sentiment`).  
  - Updates a **live Matplotlib chart** in real-time.  
  - Logs processing steps and errors for debugging.  

---

## Environment Setup
### 1. Clone repo & create virtual environment
```bash
git clone <your-repo-url>
cd buzzline-04-moses
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2 Configure environment variables

Edit .env (not committed to GitHub):

# Kafka settings
KAFKA_BROKER_ADDRESS=localhost:9092

# Project settings
PROJECT_TOPIC=project_json
PROJECT_INTERVAL_SECONDS=5
PROJECT_CONSUMER_GROUP_ID=project_group


### Running the Project

Start Zookeeper & Kafka (if running locally):
``` zsh
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

Run Producer:
``` zsh
python -m producers.project_producer_case
```
Run Consumer:
``` zsh
python -m consumers.project_consumer_mk
```

#### Visualization

The consumer displays a real-time chart:

X-axis → Timestamps of messages

Y-axis → Sentiment scores (0 to 1)

Green line with markers shows sentiment trend over time.