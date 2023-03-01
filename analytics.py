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
        print("Receving order")
        print('----------------')
        print(f'total ticket sell so far: {total_ticket_sell}')
        print(f'total revenue so far: {revenue}')


