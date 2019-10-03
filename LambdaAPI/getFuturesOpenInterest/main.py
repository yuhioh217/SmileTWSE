from src.DynamoDBController import DynamoDBController
from src.getFuturesPageData import getFuturesData

#if __name__ == "__main__":
def handler(event, context):
  _dynamodb = DynamoDBController()
  _getFutures = getFuturesData()
  _dynamodb.putdata('Stock_futures', _getFutures.getResult())