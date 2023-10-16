import json
import boto3
import uuid
import sys
from boto3.dynamodb.conditions import Key,Attr
def lambda_handler(event, context):
    tableName="bookTable"
    client = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    table = DB.Table(tableName)
    
    
    method = event["info"]["fieldName"]
    cognito_sub= event["identity"]["sub"]
    if(method=="getISBN"):
        try:
            response = table.scan(
                FilterExpression = Attr("ISBN").eq(event["arguments"]["ISBN"])
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
    if(method=="searchAllBooks"):
        try:
            if("name" in event["arguments"] and "name" != ""):
                if("LastEvaluatedKey" in event["arguments"] and event["arguments"]["LastEvaluatedKey"] != ""):
                    a = {}
                    a["ID"]=event["arguments"]["LastEvaluatedKey"]
                    response = table.scan(
                        Limit=event ["arguments"]["limit"],
                        ExclusiveStartKey = a,
                        FilterExpression = Attr("name").contains(event["arguments"]["name"])
                    )
                else:
                    response = table.scan(
                        Limit=event ["arguments"]["limit"],
                        FilterExpression = Attr("name").contains(event["arguments"]["name"])
                    )
                return response
            if("limit" in event["arguments"] and "limit" != ""):
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
    if(method == "getBook"):
        try:
            if(event["arguments"]["ID"] == ""):
                return{"ID":""}
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
                return{"ID":""}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response
        
    
    if(method == "createBook"):
        try:
            
            items = {}
            items["ID"]=uuid.uuid4().hex
            items["userId"] = cognito_sub
            for key,value in event["arguments"]["input"].items():
                items[key] = value
            
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
        
    if(method == "deleteBook"):
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
         
    if(method=="updateBook"):
        try:
            ExpressionAttributes = {}
            test = {}
            str = ""
            for key,value in event["arguments"]["input"].items():
                if(key != "ID"):
                    data_name = ":"+key
                    data_name2 = "#"+key
                    ExpressionAttributes[data_name] = value
                    test[data_name2] = key
                    str += "#"+key+"=:"+key+","
                    
            str = str[:len(str)-1]
            response = table.update_item (
                Key={
                    Primary_Column_Name:Primary_Key
                },
                UpdateExpression= 'SET '+str,
                ExpressionAttributeNames=test,
                ExpressionAttributeValues = ExpressionAttributes
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