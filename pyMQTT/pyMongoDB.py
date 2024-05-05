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

# Create a new client and connect to the server
client = MongoClient(DB_URL, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# show all databases
# print(client.list_database_names()

"""
['sample_mflix', 'admin', 'local']
sample_mflix: The sample dataset for the MongoDB Atlas cluster
"""

# show sample_mflix
db = client.MiIoT_ISE
print(db.list_collection_names())
"""
['comments', 'movies', 'sessions', 'theaters', 'users']
"""

# show sample_mflix.movies
ISE0001 = db.ISE0001

data_to_insert = {
    "title": "Your Movie Title",
    "genre": "Action",
    "release_year": 2024,
    "director": "John Doe",
    "actors": ["Actor 1", "Actor 2", "Actor 3"]
}

insert_result = ISE0001.insert_one(data_to_insert)

# 檢查是否成功插入
if insert_result.inserted_id:
    print("Data inserted successfully!")
else:
    print("Failed to insert data.")

# count the data num
print(ISE0001.count_documents({}))

"""data = movies.find_one()    # data is  dictory
# print data with putty format
for key, value in data.items():
    print(f"{key}: {value}")"""


