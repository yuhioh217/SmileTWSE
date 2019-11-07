import requests
import pandas as pd
from .mongoController import mongoController


class getBranchTrade():
    def __init__(self, broker, branch, start_date, end_date, num_type):
        self.today = end_date
        '''
          example: http://kgieworld.moneydj.com/z/zg/zgb/zgb0.djhtm?a=6010&b=6010&c=E&d=1&e=2019-10-4&f=2019-10-11
          &c=E&d=1 => stock counts
          &c=B&d=1 => stock amounts
        '''
        self.num_type = num_type
        self.url = "http://kgieworld.moneydj.com/z/zg/zgb/zgb0.djhtm?a=" + \
            broker + "&b=" + branch + "&c=" + self.num_type + \
            "&d=1&e=" + start_date + "&f=" + end_date
        self.res = requests.get(self.url)
        self.df_buy = pd.read_html(self.res.text)[3]
        self.df_sell = pd.read_html(self.res.text)[4]
        self.broker_branch = broker + "_" + branch
        self.buy_datasets = ''
        self.sell_datasets = ''
        self.db = ""

    def getBuy(self):
        # print(self.df_buy)
        self.buy_datasets = (self.df_buy.iloc[2:, [0, 1, 2, 3]]).dropna(
            thresh=3, axis=0).dropna(thresh=0, axis=1)
        # print(self.buy_datasets)
        return self.collectData(self.buy_datasets)

    def getSell(self):
        self.sell_datasets = (self.df_sell.iloc[2:, [0, 1, 2, 3]]).dropna(
            thresh=3, axis=0).dropna(thresh=0, axis=1)
        return self.collectData(self.sell_datasets)

    def collectData(self, datasets):
        idArr = []
        nameArr = []
        diffArr = []
        buyArr = []
        sellArr = []
        if len(datasets) > 1:
            for index, row in datasets.iterrows():
                if '\',\'' in row[0]:
                    id = (((row[0].split('\',\''))[0]).split('\'')[1])[2:]
                    name = ((row[0].split('\',\''))[1]).split('\'')[0]
                    buy_count = row[1]
                    sell_count = row[2]
                    diff = row[3]

                    self.db = mongoController()
                    self.db.connectDB("Brokers", "stock")
                    self.saveDataToEachStock(
                        id, name, self.broker_branch, diff)
                    idArr.append(id)
                    nameArr.append(name)
                    diffArr.append(diff)
                    buyArr.append(buy_count)
                    sellArr.append(sell_count)
                    '''
                    if self.num_type is "B":
                        print(id + " " + name + " " + buy_count +
                              " " + sell_count + " " + diff + "(仟元)")
                    if self.num_type is "E":
                        print(id + " " + name + " " + buy_count +
                              " " + sell_count + " " + diff + "(張)")
                    '''
                else:
                    print(row[0])
            '''make the json file '''
            self.db .closeDB()
            jsonObj = {
                "id": idArr,
                "name": nameArr,
                "diff": diffArr,
                "buy": buyArr,
                "sell": sellArr
            }
            return jsonObj

    '''
      JSON Data Structure
      {
        "id":"XXXX",
        "name":"XXXX",
        "data": [
          {
            "date": "20191008",
            "brokerbranch": []
            "diff": []
          }
        ]
      }
    '''

    def saveDataToEachStock(self, id, name, broker_branch, diff):
        # print(broker_branch)
        queryStockIsExist = self.db.getQueryCount({"id": id})
        # print(queryStockIsExist)
        if queryStockIsExist is 0:
            init_json = {
                "id": id,
                "name": name,
                "data": []
            }
            self.db .insertOne(init_json)

        '''' check the data in date is set or not '''
        if self.db .getQueryCount({"$and": [{"id": id}, {"data": {"$elemMatch": {"date": self.today}}}]}) is 0:
            todayJson = {
                "date": self.today,
                "diff": [],
                "brokerbranch": []
            }
            self.db .updateOne({"id": id},
                               {"$push": {"data": todayJson}}
                               )

        # todo
        isSet = self.db .getQueryCount(
            {"$and": [{"id": id}, {"data": {"$elemMatch": {"date": self.today, "brokerbranch": broker_branch}}}]})
        print(id + " " + self.today + " " + broker_branch)
        # print(isSet)
        if isSet is 0:
            self.db .updateOne({"$and": [{"id": id}, {"data": {"$elemMatch": {"date": self.today}}}]},
                               {"$push": {"data.$[].diff": diff, "data.$[].brokerbranch": self.broker_branch}})
