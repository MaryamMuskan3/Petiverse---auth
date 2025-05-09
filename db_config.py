from pymongo import MongoClient

MONGO_URI = "mongodb+srv://bismaawan003:0000@cluster0.rm3gu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.Petiverse
user_collection = db["Users"] 
