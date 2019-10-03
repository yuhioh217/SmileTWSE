import requests
import pandas as pd
pd.__file__

class getCenterID():
  def __init__(self):
    self.res = ''
    self.retry = 10
    for i in range(self.retry):
      try:
        self.res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
      except:
        if i < self.retry - 1: # i is zero indexed
          continue
        else:
          raise
      break
    
    self.df = pd.read_html(self.res.text)[0]
    self.datasets = ''
    self.idArr = []
    self.nameArr = []
    self.typeArr = []
    self.dataprocessing()

  def dataprocessing(self):
    self.datasets = (self.df.iloc[2:,[0,1,2,4]]).dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
    for index, row in self.datasets.iterrows():
      self.typeArr.append(str(row[4]))

      if '　' in row[0]:
        self.idArr.append(row[0].split('　')[0])
        self.nameArr.append(row[0].split('　')[1])
      elif ' ' in row[0]:
        self.idArr.append(row[0].split(' ')[0])
        self.nameArr.append(row[0].split(' ')[1])
      else:
        self.idArr.append('--' + row[0])
        self.nameArr.append('--' + row[0])

  def getID(self):
    return self.idArr

  def getName(self):
    return self.nameArr

  def getType(self):
    return self.typeArr
