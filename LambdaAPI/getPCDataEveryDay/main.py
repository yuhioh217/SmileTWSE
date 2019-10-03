from src.DynamoDBController import DynamoDBController
from src.getPCDataToday import getPCDataToday

#if __name__ == "__main__":
def handler(event, context):
  _dynamodb = DynamoDBController()
  _getPCData = getPCDataToday()
  _getPCData.getPostData()
  result = _getPCData.getResult()
  for r in result:
    if r['date'] is not 0:
      _dynamodb.putdata('Stock_PC_options', r)