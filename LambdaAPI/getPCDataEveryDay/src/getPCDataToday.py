import requests
import pandas as pd
import datetime
from decimal import Decimal

class getPCDataToday():
  def __init__(self):
    self.url = "http://www.taifex.com.tw/cht/3/pcRatio"
    now = datetime.datetime.now()
    self.dateToday = str(now).split(' ')[0].replace('-','/')
    self.date = ''
    self.data = ''
    self.dataArr = []
    self.datasets = ''

  def getPostData(self):
    try:
      form = {
        "queryStartDate": self.dateToday,
        "queryEndDate": self.dateToday,
      }
      self.r = requests.post(self.url, form)
      self.df = pd.read_html(self.r.text)[3]
      print(self.df)
      if len(self.df) is 0:
        print("There is no data today (" + self.dateToday + ")")
      else:
        self.datasets = (self.df.iloc[0:,[0,1,2,3,4,5,6]])
        for index, row in self.datasets.iterrows():
          self.date = row[0].split('/')[0] + ((row[0].split('/')[1]) if len((row[0].split('/')[1])) > 1 else '0' + (row[0].split('/')[1])) + ((row[0].split('/')[2]) if len((row[0].split('/')[2])) > 1 else '0' + (row[0].split('/')[2]))
          each_data = {
            'PutVolume': row[1],
            'CallVolume': row[2],
            'PCVolumeRatio': Decimal(str(row[3])),
            'PutOpenInterest': row[4],
            'CallOpenInterest': row[5],
            'PCRatio': Decimal(str(row[6])),
          }
          self.data = {
            'date': int(self.date),
            'data': each_data,
          }
          self.dataArr.append(self.data)
    except Exception as e:
      print(e)

  def getResult(self):
    return self.dataArr