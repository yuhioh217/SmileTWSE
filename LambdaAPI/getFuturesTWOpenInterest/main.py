from src.DynamoDBController import DynamoDBController
from src.getFuturesPageData import getFuturesData

#f __name__ == "__main__":
def handler(event, context):
  _dynamodb = DynamoDBController()
  _getFutures = getFuturesData()
  _dynamodb.putdata('Stock_futures_TW', _getFutures.getResult())