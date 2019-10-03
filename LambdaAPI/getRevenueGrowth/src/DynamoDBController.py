import boto3
import json
import time

class DynamoDBController():
  def __init__(self):
    self.dynamodb = boto3.resource('dynamodb', 'us-west-2')

  def putdata(self, tablename, data):
    #self.dynamodb.put_item(TableName='fruitSalad', Item={'fruitName':{'S':'Banana'},'key2':{'N':'value2'}})
    table = self.dynamodb.Table(tablename)
    table.put_item(TableName=tablename, Item=data)
  
  def delAlldata(self, tablename):
    table = self.dynamodb.Table(tablename)
    scan = table.scan(
      ProjectionExpression='#id, #name',
      ExpressionAttributeNames={
        '#id': 'id',
        '#name': 'name',
      }
    )
    
    with table.batch_writer() as batch:
      #print(scan['Items'])
      for each in scan['Items']:
        batch.delete_item(Key=each)