from src.getRevenue import getRevenue
from src.DynamoDBController import DynamoDBController
from datetime import datetime

def fetchingData(year, month):
  _dynamodb = DynamoDBController()
  _revenue = getRevenue('1', year, month)
  totalPage = _revenue.getPageCount()
  tempDataArr = []
  for i in range(1, totalPage + 1):
    _revenue.setPage(str(i))
    _revenue.fetchHtml()
    _revenue.dataprocessing()
  
  allData = _revenue.getDataArr()
  for data in allData:
    #id, name, permonth, permonthchangerate, permonthgrowthrate, cumulation, cumulationgrowthrate
    if not data.empty:
      '''
      print({
        'id': str(data[0]),
        'name': str(data[1]),
        'permonth': str(data[2]),
        'permonthchangerate': str(data[3]),
        'permonthgrowthrate': str(data[4]),
        'cumulation': str(data[5]),
        'cumulationgrowthrate': str(data[6])
      })
      '''
      tempDataArr.append({
        'id': str(data[0]),
        'name': str(data[1]),
        'permonth': str(data[2]),
        'permonthchangerate': str(data[3]),
        'permonthgrowthrate': str(data[4]),
        'cumulation': str(data[5]),
        'cumulationgrowthrate': str(data[6])
      })
      
  dataObject = {
    'date': year + month + '00',
    'data': tempDataArr
  }
  _dynamodb.putdata('StockRevenueStatus', dataObject)
  dataObject = {}


def handler(event, context):
#if __name__ == "__main__":
  strYear = ''
  strMonth = ''
  dateArr = (((datetime.now()).strftime("%Y-%m-%d %H:%M:%S")).split(' ')[0]).split('-')
  # don't to process dataArr[2] field, only check the year and month data.
  if int(dateArr[1]) is 1:
    strYear = str(int(dateArr[0])-1)
    strMonth = '12'
  else:
    strYear = dateArr[0]
    strMonth = str(int(dateArr[1])-1)
  #print(strYear, strMonth)
  fetchingData(strYear, strMonth)

  '''
  dataObject = {} # to collect date and put them to AWS DynamoDB
  strYear  = ''
  strMonth = ''
  for year in range(2019, 2020):
    strYear = str(year)
    for month in range(1, 3):
      if len(str(month)) == 1:
        strMonth = '0' + str(month)
      else:
        strMonth = str(month)
      print(strYear + strMonth + '00')
      fetchingData(strYear, strMonth)
  '''