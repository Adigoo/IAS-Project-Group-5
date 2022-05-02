import sys
import pymongo

# temp = sys.argv[0]

# print(sys.argv[0])
# print(sys.argv[1])
# print(sys.argv[2])
# print(sys.argv[3])
# print(sys.argv[4])


###################

client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"
db_name = "ias_database"
client = pymongo.MongoClient(client)
mydb = client[db_name]
vm_ips_coll = mydb["vm_ips"]


options = {"upsert": "true"}
# collection.updateOne(query, update, options);


###################

for i in range(1, 5):

    # print(i)
    # data = {
    #     "_id": sys.argv[i],
    #     "vm_name": sys.argv[i],
    #     "vm_ip": sys.argv[i + 4]
    # }
    # print(data)
    vm_ips_coll.find_one_and_update(
        {
            "_id": sys.argv[i]
        },
        {
            "$set": {
                "_id": sys.argv[i],
                "vm_name": sys.argv[i],
                "vm_ip": sys.argv[i+4]
            }
        },
        upsert=True
    )
