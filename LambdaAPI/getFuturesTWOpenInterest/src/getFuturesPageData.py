import requests
import pandas as pd
import datetime 

class getFuturesData():
  def __init__(self):
    self.queryDate = str(datetime.date.today()).replace('-','/')
    form = {
      "queryDate": self.queryDate,
      "contractId": "TX",
    }
    self.res = requests.post("http://www.taifex.com.tw/cht/3/largeTraderFutQry", form)
    #self.res = requests.get("http://www.taifex.com.tw/cht/3/largeTraderFutQry")
    self.df_date = pd.read_html(self.res.text)[2]
    self.df = pd.read_html(self.res.text)[3]
    self.date = ''
    self.data = []
    self.datasets = ''
    self.result = self.dataprocessing()


  def dataprocessing(self):
    try:
      for index, row in (self.df_date.iloc[0:,[0]]).iterrows():
        if index is 0:
          self.date = (row[0].split(' ')[0]).replace('/', '')
      '''
        English: f5n => first five number, f5p => first five present(%), toi => totalOpenInterest
        row0: name, row1: type
        row2: buy_f5n, row3: buy_f5p
        row4: buy_f10n, row5: buy_f10p
        row6: sell_f5n, row7: sell_f5p
        row8: sell_f10n, row9: sell_f10p
        row10: toi
      '''
      self.datasets = (self.df.iloc[0:,[0,1,2,3,4,5,6,7,8,9,10]]).dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
      for index, row in self.datasets.iterrows():
        #print(row[0])
        each_data = {
          'name': row[0],
          'type': row[1],
          'buy_f5n': row[2],
          'buy_f5p': row[3],
          'buy_f10n': row[4],
          'buy_f10p': row[5],
          'sell_f5n': row[6],
          'sell_f5p': row[7],
          'sell_f10n': row[8],
          'sell_f10p': row[9],
          'toi': row[10]
        }
        self.data.append(each_data)
      return {
        'date': int(self.date),
        'data': self.data
      }
    except:
      print("---")
      return {
        'message': 'empty futures data'
      }

  
  def getResult(self):
    return self.result

'''
a = getFuturesData()
print(a.getResult())
'''
