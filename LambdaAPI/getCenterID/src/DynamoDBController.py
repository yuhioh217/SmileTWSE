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

  def delAndCreateTable(self, tablename):
    table = self.dynamodb.Table(tablename)
    table.delete()
    time.sleep(20)
    #print(tablename)
    createTable = self.dynamodb.create_table(
      TableName = tablename,
      KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'name',
            'KeyType': 'RANGE'  #Sort key
        }
      ],
      AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'name',
            'AttributeType': 'S'
        },

      ],
      ProvisionedThroughput={
          'ReadCapacityUnits': 10,
          'WriteCapacityUnits': 10
      }
    )
    time.sleep(20)

'''
if __name__ == "__main__":
  a = DynamoDBController()
  a.delTable('Stock_centerID_normal')
'''
