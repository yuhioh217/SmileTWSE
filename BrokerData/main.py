from lib.getMoneyOrder import getBranchTrade
from lib.getAllBrokerBranch import getAllBroker
from lib.mongoController import mongoController
import json


def fetchAllBrokers():
    # fetch all broker and its branches to brokers.json
    _getAllBroker = getAllBroker()
    _getAllBroker.setConfigPath("./config/brokers.json")
    _getAllBroker.fetchData()


def saveConfigToMongoDB():
    # Save config data to monogDB(current is local)
    try:
        db = mongoController()
        db.connectDB("Brokers", "branches")
        with open("./config/brokers.json", 'r', encoding='utf8') as reader:
            bjson = json.loads(reader.read())
        for brokers in bjson["brokers"]:
            db.insertOne(brokers)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    with open("./config/brokers.json", 'r', encoding='utf8') as reader:
        bjson = json.loads(reader.read())
    if bjson["brokers"] is not None:
        print(json.dumps(bjson["brokers"][0], ensure_ascii=False))
        _getTrade = getBranchTrade(bjson["brokers"][0]["id"],
                                   bjson["brokers"][0]["branches"][0], "B")
        _getTrade.getSell()
