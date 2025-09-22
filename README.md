## Project Consumer (MK)

This custom consumer (`project_consumer_mk.py`) reads messages from the Kafka topic **`buzzline_json`**.  
It visualizes the **sentiment trend over time** in real time.  

### What It Does
- Consumes live JSON messages produced by `project_producer_case.py`.  
- Extracts the `timestamp` and `sentiment` fields from each message.  
- Appends them into two lists to track sentiment scores over time.  
- Updates a **line chart** that shows how positive or negative the stream of messages is as they arrive.  

### Why This Is Interesting
Sentiment analysis gives insight into the overall “mood” of the messages.  
Plotting sentiment values as a **line chart** over time shows live trends — whether messages are getting more positive or negative — making it more dynamic and meaningful than static counts.  

### Run Instructions

Start the provided producer (do not modify):
``` zsh
python3 -m producers.project_producer_case
```

Run my custom consumer:
``` zsh 
python3 -m consumers.project_consumer_mk
``` 

### Visualization

Chart Type: Line chart

X-axis: Message timestamps

Y-axis: Sentiment scores

Chart Title: "Real-Time Sentiment Trend - MK"
