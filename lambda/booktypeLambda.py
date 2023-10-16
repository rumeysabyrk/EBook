import json
import boto3
import uuid
import sys
from boto3.dynamodb.conditions import Key,Attr
def lambda_handler(event, context):
    tableName="bookTypeTable"
    client = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    table = DB.Table(tableName)
    
    
    method = event["info"]["fieldName"]
    if(method== "listBookTypes"):
        try:
            if("LastEvaluatedKey" in event["arguments"] and event["arguments"]["LastEvaluatedKey"] != ""):
                a = {}
                a["ID"]=event["arguments"]["LastEvaluatedKey"]
                response = table.scan(
                    Limit=event ["arguments"]["limit"],
                    ExclusiveStartKey = a
                )
            else:
                response = table.scan(
                    Limit=event ["arguments"]["limit"]
                )
                
            return response
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response
        
    if(method == "getBookType"):
        try:
            if(event["arguments"]["ID"] == ""):
                return {"ID":""}
            Primary_Column_Name = "ID"
            Primary_Key = event["arguments"]["ID"]
            response = table.get_item(
                Key={
                    Primary_Column_Name:Primary_Key
                }
            )
            if("Item" in response):
                return response["Item"]
            else:
                return {"ID":""}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response
    if(method=="createBookType"):
        try:
            items = {}
            for key,value in event["arguments"]["input"].items():
                items[key] = value
            items["ID"]=str(uuid.uuid4())
            response = table.put_item(
                Item = items
            )
            
            response_data = {
                "status":response["ResponseMetadata"]["HTTPStatusCode"], 
                "message":"Başarılı"
            }
            
            return response_data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response
    Primary_Column_Name = "ID"
    Primary_Key = event["arguments"]["input"]["ID"]
    if(method=="deleteBookType"):
        try:
            response = table.delete_item(
                Key={
                    Primary_Column_Name:Primary_Key
                }
            )
            response_data = {
                "status":response["ResponseMetadata"]["HTTPStatusCode"], 
                "message":"Başarılı"
            }
            
            return response_data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response
    if(method=="updateBookType"):
        try:
            response = table.update_item (
                Key={
                    Primary_Column_Name:Primary_Key
                },
                UpdateExpression= 'SET #name= :name',
                ExpressionAttributeNames={"#name":"name"},
                ExpressionAttributeValues = {":name":event["arguments"]["input"]["name"]}
            )
            
            response_data = {
                "status":response["ResponseMetadata"]["HTTPStatusCode"], 
                "message":"Başarılı"
            }
            
            return response_data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response