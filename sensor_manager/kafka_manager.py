import logging
from time import sleep
import kafka
# import kafka_manager
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import sensor_data
import threading
import sensor_db
import requests
import pymongo


# localhost_ip_address = "172.17.0.1"
pub_ip = requests.get("http://api.ipify.org").content.decode()
localhost_ip_address = pub_ip
# localhost_ip_address = "localhost"


##################

client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"
db_name = "ias_database"
client = pymongo.MongoClient(client)
mydb = client[db_name]
vm_ips_coll = mydb["vm_ips"]

actual_config = vm_ips_coll.find_one(
    {"_id": "kafkavm"}
)

# print(actual_config)
kafka_vm_ip = actual_config["vm_ip"]
kafka_vm_ip = kafka_vm_ip.replace('"', '')
# to remove redundant double quotes

##################


# bootstrap_servers = [f'{localhost_ip_address}:9092']
bootstrap_servers = [f'{kafka_vm_ip}:9092']

################################# KAFKA CREATE/PRODUCE/CONSUME #########################################


def create_kafka_topic(topic_name):
    '''Creates Kafka topic'''
    consumer = KafkaConsumer(topic_name,
                             bootstrap_servers=bootstrap_servers,
                             auto_offset_reset='earliest')


def produce_data(topic_name):
    '''Produces data and store into the topic'''
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    while(True):
        data = sensor_data.produceData(topic_name)
        producer.send(topic_name, bytes(str(data), 'utf-8'))
        sleep(30)


def consume_data(topic_name):
    tp = TopicPartition(topic_name, 0)
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
    consumer.assign([tp])
    consumer.seek_to_beginning(tp)

    # obtain the last offset value
    lastOffset = consumer.end_offsets([tp])[tp]

    data = []
    for message in consumer:
        msg = message[6].decode('utf-8')
        data.append(msg)
        if message.offset == lastOffset - 1:
            break

    return data

######################################## PRODUCE DATA FOR ALL SENSORS ##################################


def produce_sensors_data():
    logging.warning("STARTED PRODUCING DATA...")
    sensor_instances = sensor_db.get_all_sensor_instances()
    for instance in sensor_instances:
        # Creating thread for each sensor instance present in the mongodb
        topic_name = instance['sensor_type'] + '_' + str(instance['_id'])
        create_kafka_topic(topic_name)
        threading.Thread(target=produce_data, args=(topic_name,)).start()
