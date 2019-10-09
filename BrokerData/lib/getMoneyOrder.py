import requests
import pandas as pd


class getMoney():
    def __init__(self):
        self.res = requests.get(
            "http://kgieworld.moneydj.com/z/zg/zgb/zgb0.djhtm?a=9600&b=9658&c=B&e=2019-3-25&f=2019-3-25")
        self.df_buy = pd.read_html(self.res.text)[3]
        self.df_sell = pd.read_html(self.res.text)[4]
        self.datasets = ''

    def getID(self):
        self.datasets = (self.df_buy.iloc[2:, [0, 1, 2, 3]]).dropna(
            thresh=3, axis=0).dropna(thresh=3, axis=1)
        for index, row in self.datasets.iterrows():
            if '\',\'' in row[0]:
                id = (((row[0].split('\',\''))[0]).split('\'')[1])[2:]
                name = ((row[0].split('\',\''))[1]).split('\'')[0]
                print(id + name)
            else:
                print(row[0])
        return self.datasets
