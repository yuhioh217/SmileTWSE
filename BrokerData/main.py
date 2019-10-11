from lib.getMoneyOrder import getBranchTrade
from lib.getAllBrokerBranch import getAllBroker
from lib.mongoController import mongoController
import json
from datetime import date


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
    # today = (date.today()).strftime("%Y-%m-%d")
    today = "2019-10-09"
    db = mongoController()
    db.connectDB("Brokers", "trading")

    with open("./config/brokers.json", 'r', encoding='utf8') as reader:
        bjson = json.loads(reader.read())

    if bjson["brokers"] is not None:
        ''' initial the database structure to each broker's branch'''
        for i, broker in enumerate(bjson["brokers"]):
            branches = bjson["brokers"][i]["branches"]
            for j, branch in enumerate(branches):
                brokerBranch = bjson["brokers"][i]["id"] + \
                    "_" + bjson["brokers"][i]["branches"][j]

                # initial broker item
                queryCount = db.getQueryCount({"brokerBranch": brokerBranch})
                if queryCount is 0:
                    init_json = {
                        "brokerBranch": brokerBranch,
                        "data": []
                    }
                    db.insertOne(init_json)

                # print(json.dumps(bjson["brokers"][0], ensure_ascii=False))
                _getTrade = getBranchTrade(bjson["brokers"][0]["id"],
                                           bjson["brokers"][0]["branches"][0], today, today, "B")
                jsonObj = {
                    "date": today,
                    "buy": _getTrade.getBuy(),
                    "sell": _getTrade.getSell()
                }

                ''' check the data in date is set or not '''
                isSet = db.getQueryCount({"brokerBranch": brokerBranch,
                                          "data": {"$elemMatch": {"date": today}}})
                if isSet is 0:
                    db.updateOne({"brokerBranch": brokerBranch},
                                 {"$push": {"data": jsonObj}})
                # print(jsonObj)

    db.closeDB()
