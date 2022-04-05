import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
)

my_cursor = mydb.cursor()

my_cursor.ececute("CREATE DATABASE Users")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)
