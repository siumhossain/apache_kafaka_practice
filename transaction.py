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
            "price":consumed_message["price"]
        }
        producer.send("analytics", json.dumps(data).encode("utf-8"))
        print("Successful transaction..")
