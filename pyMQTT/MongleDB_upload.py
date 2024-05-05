"""
MongoDB cloud Atlas
"""
# STL CA
import certifi

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

USER = "Admin"
PASSWORD = "03734301"
DB_URL = f"mongodb+srv://{USER}:{PASSWORD}"
DB_URL += "@ntu-miiot-bk.jfvrs61.mongodb.net/?retryWrites=true&w=majority&appName=NTU-MiIoT-BK"

class MongleDB:
    # 初始化方法，用於初始化類的屬性
    def __init__(self):
        self.client = MongoClient(DB_URL, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
    
        """self.db = self.client.MiIoT_ISE
        self.ISE0001 = self.db.ISE0001
        self.ISE0002 = self.db.ISE0002
        self.ISE0003 = self.db.ISE0003
        self.ISE0004 = self.db.ISE0004
        self.ISE0005 = self.db.ISE0005"""
    
    def insert_data(self,collection_name,msg):
        db = self.client.MiIoT_ISE
        #collection = getattr(self, collection_name)
        co = getattr(db,collection_name)
        #co = db.collection
        insert_result = co.insert_one(msg)
        if insert_result.inserted_id:
            print("Data inserted successfully!")
        else:
            print("Failed to insert data.")

    def insert_data_env(self,collection_name,msg):
        db = self.client.MiIoT_ENV
        co = getattr(db,collection_name)
        insert_result = co.insert_one(msg)
        if insert_result.inserted_id:
            print("Data inserted successfully!")
        else:
            print("Failed to insert data.")
    

"""def connect_to_MongleDB():
    # Create a new client and connect to the server
    client = MongoClient(DB_URL, server_api=ServerApi('1'), tlsCAFile=certifi.where())

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    db = client.MiIoT_ISE
    ISE0001 = db.ISE0001
    ISE0002 = db.ISE0002
    ISE0005 = db.ISE0005"""

# show all databases
# print(client.list_database_names()


#db = client.MiIoT_ISE
#print(db.list_collection_names())
"""
['comments', 'movies', 'sessions', 'theaters', 'users']
"""

# show sample_mflix.movies
#ISE0001 = db.ISE0001


#insert_result = ISE0001.insert_one(data_to_insert)

# 檢查是否成功插入
"""if insert_result.inserted_id:
    print("Data inserted successfully!")
else:
    print("Failed to insert data.")"""

# count the data num
#print(ISE0001.count_documents({}))

"""data = movies.find_one()    # data is  dictory
# print data with putty format
for key, value in data.items():
    print(f"{key}: {value}")"""


