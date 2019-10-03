import requests
import pandas as pd

class getCenterID():
  def __init__(self):
    self.res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    self.df = pd.read_html(self.res.text)[0]
    self.datasets = ''
    self.idArr = []
  
  def getID(self):
    self.datasets = (self.df.iloc[2:,[0,1,2]]).dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
    for index, row in self.datasets.iterrows():
      if '　' in row[0]:
        self.idArr.append(row[0].split('　')[0])
      elif ' ' in row[0]:
        self.idArr.append(row[0].split(' ')[0])
      else:
        self.idArr.append('--' + row[0])
    return self.idArr
     

if __name__ == "__main__":
    a = getCenterID()
    print(a.getID())