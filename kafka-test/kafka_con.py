#!/usr/bin/env python
# encoding:utf8
from pykafka import KafkaClient

# from kafka import KafkaConsumer
# connect to Kafka server and pass the topic we want to consume
# consumer = KafkaConsumer('666', bootstrap_servers=['192.168.1.139:9092', '192.168.1.140:9092'])
# for msg in consumer:
#    print(msg)

client = KafkaClient(hosts='192.168.1.139:9092, 192.168.1.140:9092, 192.168.1.152:9092')
topic = client.topics[bytes('box0', 'utf-8')]
consumer = topic.get_simple_consumer(
    #    consumer_group="666",
    #    auto_offset_reset=OffsetType.EARLIEST,
    reset_offset_on_start=True
)
for message in consumer:
    if message is not None:
        print(message.offset, message.value)

print('end')
