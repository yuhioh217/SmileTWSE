import requests
import pandas as pd
import time
import calendar
from DynamoDBController import DynamoDBController

class getFuturesHistoryData():
  def __init__(self, date):
    self.queryDate = date
    self.contractId = "TX"
    self.url = "http://www.taifex.com.tw/cht/3/largeTraderFutQry"
    self.r = ''
    self.df_date = ''
    self.df = ''
    self.data = []


  def getPostData(self):
    try:
      form = {
        "queryDate": self.queryDate,
        "contractId": self.contractId,
      }
      self.r = requests.post(self.url, form)
      self.df_date = pd.read_html(self.r.text)[2]
      self.df = pd.read_html(self.r.text)[3]
      #print(self.datasets)
    except Exception as e:
      print(e)

  def dataprocessing(self):
    try:
      for index, row in (self.df_date.iloc[0:,[0]]).iterrows():
        if index is 0:
          self.date = (row[0].split(' ')[0]).replace('/', '')
      print(self.date)
      self.datasets = (self.df.iloc[0:,[0,1,2,3,4,5,6,7,8,9,10]]).dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
      #print(self.datasets)
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
      print(self.queryDate + ' no data')
      return {
        'date': 0,
        'message': 'empty futures data'
      }


if __name__ == "__main__":
  yearArr = [2019]
  monthArr = [1,2,3,4]
  cal = calendar.Calendar()
  dateArr = []
  _dynamodb = DynamoDBController()
  for year in yearArr:
    for month in monthArr:
      for day in cal.itermonthdays(year, month):
        if str(day) != "0":
          tempYearStr = str(year)
          tempMonthStr = "0" + str(month) if len(str(month)) is 1 else str(month)
          tempdayStr = "0" + str(day) if len(str(day)) is 1 else str(day)
          tempDateStr = tempYearStr + "/" +tempMonthStr + "/" + tempdayStr
          dateArr.append(tempDateStr)
      for date in dateArr:
        _Object = getFuturesHistoryData(date)
        _Object.getPostData()
        resultJSON = _Object.dataprocessing()
        if resultJSON['date'] is not 0:
          _dynamodb.putdata('Stock_futures_TW', resultJSON)
      dateArr = []
  '''
  _Object = getFuturesHistoryData("2019/03/17")
  _Object.getPostData()
  resultJSON = _Object.dataprocessing()
  time.sleep(5)
  '''