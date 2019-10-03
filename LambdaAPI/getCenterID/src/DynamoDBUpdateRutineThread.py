import threading
from .DynamoDBController import DynamoDBController
from datetime import datetime

class DynamoDBUpdateRutineThread(threading.Thread):
  tlist = []
  maxThread = 50
  event = threading.Event()
  lck = threading.Lock()

  def __init__(self, table ,data, start_time):
    threading.Thread.__init__(self)
    self.table = table
    self.data  = data
    self.start_time = start_time
    self._dynamoDB = DynamoDBController()
  
  def getCurrentData(self):
    return self.data

  def run(self):
    self._dynamoDB.putdata(self.table , self.data)
    DynamoDBUpdateRutineThread.lck.acquire()
    DynamoDBUpdateRutineThread.tlist.remove(self)
    if len(DynamoDBUpdateRutineThread.tlist)==DynamoDBUpdateRutineThread.maxThread-1:
        DynamoDBUpdateRutineThread.event.set()
        DynamoDBUpdateRutineThread.event.clear()
    DynamoDBUpdateRutineThread.lck.release()
  
    if self.table is 'Stock_centerID_BSecurities':
      print(len(DynamoDBUpdateRutineThread.tlist))
      if len(DynamoDBUpdateRutineThread.tlist) is 0:
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._dynamoDB.putdata('Status_table', {'status': 'get_center_id', 'start_time': self.start_time,'end_time': end_time , 'updateing': False})


  def newthread(table, data, start_time):
    DynamoDBUpdateRutineThread.lck.acquire()#上鎖
    sc=DynamoDBUpdateRutineThread(table, data, start_time)
    DynamoDBUpdateRutineThread.tlist.append(sc)
    DynamoDBUpdateRutineThread.lck.release()#解鎖
    sc.start()
  newthread=staticmethod(newthread)
