from src.FirstStep import FirstStep
from src.DynamoDBController import DynamoDBController
from src.DynamoDBUpdateRutineThread import DynamoDBUpdateRutineThread
from datetime import datetime
import logging
import json
import queue
import boto3
import threading

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#def handler(event, context):
if __name__ == "__main__":
  # First, we should fetch all center stock ID. (I will get an array from getCenterID().getID())

  _first = FirstStep()
  _centerIDArr = _first.getID()
  _centerName  = _first.getName()
  _centerType  = _first.getType()
  currentTable = 'Stock_centerID_normal' # default Table
  Thread_list = []
  task_queue = queue.Queue()

  json_str_id = {
    "centerID": _centerIDArr
  }

  json_str_name = {
    "centerName": _centerName
  }

  json_str_type = {
    "centerType": _centerType
  }

  _dynamoDB = DynamoDBController()
  start_time = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
  _dynamoDB.putdata('Status_table', {'status': 'get_center_id', 'start_time': start_time, 'end_time': '-' , 'updateing': True})
  #_dynamoDB.delAndCreateTable(currentTable)
  threads = []
  for (_id, _name, _type) in zip(json_str_id.get("centerID"), json_str_name.get('centerName'), json_str_type.get('centerType')):
    if '--' in _id:
      if '上市認購(售)權證' in _id:
        currentTable = 'Stock_centerID_warrant'
      elif '特別股' in _id:
        currentTable = 'Stock_centerID_special'
      elif 'ETF' in _id:
        currentTable = 'Stock_centerID_ETF'
      elif '臺灣存託憑證(TDR)' in _id:
        currentTable = 'Stock_centerID_TDR'
      elif '受益證券-不動產投資信託' in _id:
        currentTable = 'Stock_centerID_BSecurities'
      else:
        currentTable = 'Stock_centerID_normal'
      logger.info('Delete and create table : {}'.format(currentTable))
      _dynamoDB.delAndCreateTable(currentTable)
    else:
      DynamoDBUpdateRutineThread.lck.acquire()
      if len(DynamoDBUpdateRutineThread.tlist)>=DynamoDBUpdateRutineThread.maxThread:
        DynamoDBUpdateRutineThread.lck.release()
        DynamoDBUpdateRutineThread.event.wait()#scanner.evnt.set()遇到set事件則等待結束
      else:
        DynamoDBUpdateRutineThread.lck.release()
      if currentTable is 'Stock_centerID_normal':
        DynamoDBUpdateRutineThread.newthread(currentTable, {'id':_id, 'name':_name, 'type': _type}, start_time)
      if currentTable != 'Stock_centerID_warrant' and currentTable != 'Stock_centerID_normal':
        DynamoDBUpdateRutineThread.newthread(currentTable, {'id':_id, 'name':_name}, start_time)
      #print(len(DynamoDBUpdateRutineThread.tlist))

  #return {
  #  'message': 'Update the latest id info.'
  #}
