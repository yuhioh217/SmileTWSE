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

    def getQueryCount(self, json):
        if self.collection is not None:
            return self.collection.count_documents(json)

    def insertOne(self, json):
        if self.collection is not None:
            self.collection.insert_one(json)

    def updateOne(self, query, json):
        '''
          add the json file to jsonArray use $push
          add the json file to value use $set
          find the json in arr use $elemMatch
        '''
        self.collection.update_one(query, json)

    def closeDB(self):
        self.client.close()
