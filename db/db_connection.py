import pymongo
from pymongo import MongoClient

MONGODB_URI = "mongodb://localhost:27017"

cluster = MongoClient(MONGODB_URI)
database = cluster["database"]
collection = database["collection"]
