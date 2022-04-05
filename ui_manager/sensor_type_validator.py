import json
import uuid


# def read_db_configuration(filepath):
#     print("in read_db_configureation")
#     print(filepath)
#     f = open(filepath, "r")

#     # Reading from file
#     data = json.loads(f.read())
#     print(data)
#     host_name = data["host"]
#     user_name = data["user"]
#     password = data["password"]
#     database_name = data["database"]
#     return host_name, user_name, password, database_name


# def insert_data_to_table(tablename, table_column_names, row_data):
#     print(f"in insert data {tablename}")
#     filepathdb = "configurations/db_config.json"
#     host_name, user_name, password, database_name = read_db_configuration(
#         filepathdb)

#     print(host_name, user_name, password, database_name)
#     mydb = mysql.connector.connect(
#         host=host_name,
#         user=user_name,
#         password=password,
#         database=database_name
#     )

#     print("connection successful")
#     mycursor = mydb.cursor()

#     table_column_str = ", ".join(i for i in table_column_names)
#     sql = "INSERT INTO "+tablename + \
#         " ("+ table_column_str +") VALUES ("+str(row_data)[1:-1]+")"

#     mycursor.execute(sql)

#     mydb.commit()


def sensor_type_validator(filepath):
    with open(filepath, "r") as read_content:
        print("FILE CONTENT in validator")
        # print(json.load(read_content))

        file_content = json.load(read_content)
        print(file_content)

        uuidstr = str(uuid.uuid4())

        file_new_name = "sensor_type_" + uuidstr + ".json"

        sensor_type_id = "sensor_type_" + uuidstr
        sensor_type = file_content['sensor_type']

        # insert_data_to_table('sensor_types',
        #     ['sensor_type_id', 'sensor_type'],
        #     [sensor_type_id, sensor_type]
        # )

        return True
