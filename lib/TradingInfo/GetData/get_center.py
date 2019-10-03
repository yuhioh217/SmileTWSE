from threading import Thread
import numpy
import time
import requests

# getCenterID's getID(return idArr) -> CenterParser getStockInfo
class CenterParser(Thread):
  # http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_3040.tw|tse_6116.tw&json=1&delay=0&_=1551582956854
  def __init__(self, idArr):
    Thread.__init__(self)
    self.url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp"
    self.cookie = "http://mis.twse.com.tw/stock/fibest.jsp?lang=zh_tw"
    self.session = self.fetch_cookies()
    self.idArr = idArr

  def fetch_cookies(self):
    _session = requests.session()
    _session.get(self.cookie)
    return _session

  def update_session(self):
    r = (self.session).get(self.cookie)
    if r.cookies.get_dict():
      (self.session).cookies.update(r.cookie)