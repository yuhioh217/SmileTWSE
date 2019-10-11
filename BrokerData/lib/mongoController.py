import json
from pymongo import MongoClient


class mongoController():
    def __init__(self):
        self.db = ""
        self.collection = ""
        # connect to local mongoDB
        self.client = MongoClient('localhost', 27017)

    def connectDB(self, db, col):
        if self.client is not None:
            self.db = self.client[db]
            self.collection = self.db[col]

    def insertOne(self, json):
        if self.collection is not None:
            self.collection.insert_one(json)
