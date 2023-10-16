import json
import boto3
import uuid
import sys
from boto3.dynamodb.conditions import Key,Attr
def lambda_handler(event, context):
    tableName="ageTable"
    client = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    table = DB.Table(tableName)
    
    
    method = event["info"]["fieldName"]
    if(method=="listAges"):
        try:
            response = table.scan()
            return response["Items"]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response
    if(method == "getAge"):
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
    
    if(method=="createAge"):
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
    if(method =="updateAge"):
        try:
            response = table.update_item (
                Key={
                    Primary_Column_Name:Primary_Key
                },
                UpdateExpression= 'SET #age= :age',
                ExpressionAttributeNames={"#age":"age"},
                ExpressionAttributeValues = {":age":event["arguments"]["input"]["age"]}
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
    if(method=="deleteAge"):
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