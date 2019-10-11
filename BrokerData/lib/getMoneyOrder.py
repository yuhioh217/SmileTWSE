import requests
import pandas as pd


class getBranchTrade():
    def __init__(self, broker, branch, num_type):
        '''
          &c=E&d=1 => stock counts
          &c=B&d=1 => stock amounts
        '''
        self.num_type = num_type
        self.url = "http://kgieworld.moneydj.com/z/zg/zgb/zgb0.djhtm?a=" + \
            broker + "&b=" + branch + "&c=" + self.num_type + \
            "&d=1"  # + "&c=B&e=2019-3-25&f=2019-3-25"
        self.res = requests.get(self.url)
        self.df_buy = pd.read_html(self.res.text)[3]
        self.df_sell = pd.read_html(self.res.text)[4]
        self.buy_datasets = ''
        self.sell_datasets = ''

    def getBuy(self):
        self.buy_datasets = (self.df_buy.iloc[2:, [0, 1, 2, 3]]).dropna(
            thresh=3, axis=0).dropna(thresh=3, axis=1)
        self.collectData(self.buy_datasets)
        return self.buy_datasets

    def getSell(self):
        self.sell_datasets = (self.df_sell.iloc[2:, [0, 1, 2, 3]]).dropna(
            thresh=3, axis=0).dropna(thresh=3, axis=1)
        self.collectData(self.sell_datasets)
        return self.sell_datasets

    def collectData(self, datasets):
        if len(datasets) > 0:
            print(datasets)
            for index, row in datasets.iterrows():
                if '\',\'' in row[0]:
                    id = (((row[0].split('\',\''))[0]).split('\'')[1])[2:]
                    name = ((row[0].split('\',\''))[1]).split('\'')[0]
                    buy_count = row[1]
                    sell_count = row[2]
                    diff = row[3]
                    if self.num_type is "B":
                        print(id + " " + name + " " + buy_count +
                              " " + sell_count + " " + diff + "(仟元)")
                    if self.num_type is "E":
                        print(id + " " + name + " " + buy_count +
                              " " + sell_count + " " + diff + "(張)")
                else:
                    print(row[0])
