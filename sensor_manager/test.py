import pymongo, requests




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

##################

print(kafka_vm_ip)
kafka_vm_ip = kafka_vm_ip.replace('"', '')
print(kafka_vm_ip)

bootstrap_servers = [f'{kafka_vm_ip}:9092']

print(bootstrap_servers[0])