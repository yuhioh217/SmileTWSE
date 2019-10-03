import pandas as pd
import math
from lxml import html
import requests

class getRevenue():
  retry = 3 #if the url timeout, will retry 3 times
  def __init__(self ,page ,year, month):
    '''
      Construct a new 'getRevenue' object.
      :param page: The page of website
      :param year: The year that you want to get
      :param month: The month that you want to get
    '''
    self.page = page
    self.year = year
    self.month = month
    self.res = ''
    self.df  = ''
    self.url = ''
    self.totalPage = 0
    self.datasets = ''
    self.dataArr = []
    self.setUrl()

  def setUrl(self):
    self.url = "https://www.cnyes.com/twstock/financial2.aspx?pi={}&param={}%E5%B9%B4{}%E6%9C%88&datetype=ALL&market=T".format(self.page, self.year, self.month)

  def setPage(self, page):
    self.page = page
    self.setUrl()

  def setTime(self, year, month):
    self.year = year
    self.month= month
    self.setUrl()

  def fetchHtml(self):
    try:
      #https://www.cnyes.com/twstock/financial2.aspx?pi=1&param=2018%E5%B9%B411%E6%9C%88&datetype=ALL&market=T
      for i in range(self.retry):
        try:
          self.res = requests.get(self.url)
          self.df = pd.read_html(self.res.text)[0]
        except:
          if i < self.retry - 1: # i is zero indexed
            continue
          else:
            raise
        break
    except:
      print('Fetching Data failed.')
    
 
  def dataprocessing(self):
    self.datasets = (self.df.iloc[0:,[0,1,2,3,4,5,6]]).dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
    for index, row in self.datasets.iterrows():
      self.dataArr.append(row)

  def getPageCount(self):
    self.res = requests.get(self.url)
    parsed_page = html.fromstring(self.res.content)
    text = parsed_page.xpath('//div[@class="TableFoot"]/div[@id="ctl00_ContentPlaceHolder1_div_pageinfo"]/cite/text()')
    self.totalPage = math.ceil(int(text[2])/30)
    return self.totalPage

  def getDataArr(self):
    return self.dataArr
