from lib.getMoneyOrder import getMoney
from lib.getAllBrokerBranch import getAllBroker
import json

if __name__ == "__main__":
    _getAllBroker = getAllBroker()
    _getAllBroker.setConfigPath("./config/brokers.json")
    _getAllBroker.fetchData()
