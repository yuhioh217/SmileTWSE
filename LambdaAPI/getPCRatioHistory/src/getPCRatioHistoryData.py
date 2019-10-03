import requests
import pandas as pd
import time
import calendar
from decimal import Decimal
from DynamoDBController import DynamoDBController

class getPCRatioHistoryData():
  def __init__(self, dateStr, db):
    self.proidDate = dateStr
    self.contractId = "TX"
    self.url = "http://www.taifex.com.tw/cht/3/pcRatio"
    self.r = ''
    self.df_date = ''
    self.df = ''
    self.data = []
    self.queryStartDate = (self.proidDate).split('-')[0]
    self.queryEndDate = (self.proidDate).split('-')[1]
    self._dynamodb = db

  def getPostData(self):
    try:
      form = {
        "queryStartDate": self.queryStartDate,
        "queryEndDate": self.queryEndDate,
      }
      self.r = requests.post(self.url, form)
      self.df = pd.read_html(self.r.text)[3]
      #print(self.df)
    except Exception as e:
      print(e)

  def dataprocessing(self):
    try:
      self.datasets = (self.df.iloc[0:,[0,1,2,3,4,5,6]]).dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
      #print(self.datasets)
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
        data = {
          'date': int(self.date),
          'data': each_data,
        }
        if data['date'] is not 0:
          self._dynamodb.putdata('Stock_PC_options', data)
    except:
      return {
        'date': 0,
        'message': 'there is no data',
      }



if __name__ == "__main__":
  yearArr = [2019]
  monthArr = [1,2,3,4]
  cal = calendar.Calendar()
  dateArr = []
  _dynamodb = DynamoDBController()
  dayCount = 0
  priodDateStr = ''
  for year in yearArr:
    for month in monthArr:
      for day in cal.itermonthdays(year, month):
        if str(day) != "0":
          dayCount = dayCount + 1
          '''
          tempYearStr = str(year)
          tempMonthStr = "0" + str(month) if len(str(month)) is 1 else str(month)
          tempdayStr = "0" + str(day) if len(str(day)) is 1 else str(day)
          tempDateStr = tempYearStr + "/" +tempMonthStr + "/" + tempdayStr
          dateArr.append(tempDateStr)
          '''
      tempYearStr = str(year)
      tempMonthStr = "0" + str(month) if len(str(month)) is 1 else str(month)
      priodDateStr = tempYearStr + "/" +tempMonthStr + "/01-" +  tempYearStr + "/" +tempMonthStr + "/" + str(dayCount)
      dateArr.append(priodDateStr)
      priodDateStr = ''
      dayCount = 0

      for date in dateArr:
        print(date)
        _Object = getPCRatioHistoryData(date, _dynamodb)
        _Object.getPostData()
        resultJSON = _Object.dataprocessing()
      time.sleep(1)
      dateArr = []