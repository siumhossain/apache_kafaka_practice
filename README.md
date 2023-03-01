# apache_kafaka_practice
**Apache Kafka** is a distributed event store and stream-processing platform. It is an open-source system developed by the Apache Software Foundation written in Java and Scala. The project aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds.

We are gonna build a simple ticket buying system just to understand basic consumer and producer functionality in **Kafka**

![kafka_output](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/48t2r2sncbm7i1frerwv.gif)

First of all we need to setup kafka, zookeeper and python kafka package.

For kafka and zookeeper I'm using docker for installation. Here is the `docker-compose.yml` file 
```yml
version: '2'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - 22181:2181
  kafka:
    image: confluentinc/cp-kafka:5.3.1
    depends_on:
      - zookeeper
    ports:
      - 29092:29092
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```
And also you have to install [kafka-python-package](https://kafka-python.readthedocs.io/en/master/)

```bash
pip install kafka-python
```

All things done! Let's get into coding

#### Summary
Let's think from frontend, suppose user will request of buying ticket from fronted, behind the scene our `kafka` producer will send streams of data to the Kafka cluster with respected data. And one `kafka` consumer will allows applications to read streams of data from the cluster. And we can make as producer and consumer API as much as we need for different different task.

#### Code 
> producer.py
```py
import json
from faker import Faker
# faker package just use for some random data

fake = Faker() 
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:29092")
for i in range(40_000):

    data = {
        "tiket_id":id,
        "user_id": fake.name(),
        "price": 100,
        "bank_account": fake.bban()
    }

    producer.send("order_details", json.dumps(data).encode("utf-8"))
# order details: is just an event name in kafka cluster
    print(f"done sending ..{i}")
```

> transaction.py responsible for receiving those data and build another producer in kafka cluster just for calculation total revenue and total amount of sold ticket

```py
from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_TOPIC = "order_details"

producer = KafkaProducer(bootstrap_servers="localhost:29092")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers="localhost:29092"
)

print('start listening"')

while True:
    for i in consumer:
        print('ongoing transaction')
        consumed_message = json.loads(i.value.decode())
        data = {
            "price":consumed_message["price"] #retrieve price data from previous producer which is now in kafka cluster 
        }

        producer.send("analytics", json.dumps(data).encode("utf-8")) #then just demo purpose I created another producer for calculation
        print("Successful transaction..")
```
> analytics.py
```py
from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_TOPIC = "analytics"
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers="localhost:29092"
)
print('start listening"')

while True:
    total_ticket_sell = 0
    revenue = 0
    for i in consumer:
        consumed_message = json.loads(i.value.decode())
        total_ticket_sell += 1
        revenue += consumed_message['price']
        print("============\n\n")
        print("Receiving order")
        print('----------------')
        print(f'total ticket sell so far: {total_ticket_sell}')
        print(f'total revenue so far: {revenue}')


```
Done, now time for testing. Keep in mind you run your docker compose file and 3 python file in 3 different terminal just to see what happening.

> N:B run 2 consumer file at first, then the producer.py file

![kafka_output](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/48t2r2sncbm7i1frerwv.gif)
