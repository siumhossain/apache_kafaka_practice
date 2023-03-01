import json
from faker import Faker


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
    print(f"done sending ..{i}")