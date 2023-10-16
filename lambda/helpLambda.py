import json
import boto3
import uuid
import sys
from boto3.dynamodb.conditions import Key,Attr
def lambda_handler(event, context):
    tableName="questionTable"
    helpName="helpTable"
    client = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    table = DB.Table(tableName)
    helpTable = DB.Table(helpName)
    
    method = event["info"]["fieldName"]
    if(method=="communication"):
        try:
            response={
                "phone":"+098505321603",
                "email":"hello@kuark.co",
                "address":"Konak Mah. Yayla Sk. No:9,16110 Nilüfer/Bursa"
            }
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
    if(method=="searchQuestion"):
        try:
            if("LastEvaluatedKey" in event["arguments"] and event["arguments"]["LastEvaluatedKey"] != ""):
                    a = {}
                    a["ID"]=event["arguments"]["LastEvaluatedKey"]
                    response = table.scan(
                        Limit=event ["arguments"]["limit"],
                        ExclusiveStartKey = a,
                        FilterExpression = Attr("title").contains(event["arguments"]["title"])
                    )
            else:
                response = table.scan(
                    Limit=event ["arguments"]["limit"],
                    FilterExpression = Attr("title").contains(event["arguments"]["title"])
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
    if(method=="getHelpName"):
        try:
            response = helpTable.scan()
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
    if(method=="getQuestion"):
        try:
            
            response = table.scan(
                FilterExpression = Attr("type").eq(event["arguments"]["type"])
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
    if(method=="createHelp"):
        try:
            if(event["arguments"]["input"]["name"] == ""):
                response_data = {
                    "status":204, 
                    "message":"İsim giriniz"
                }
            
                return response_data
            items = {}
            items["ID"]=uuid.uuid4().hex
            for key,value in event["arguments"]["input"].items():
                items[key] = value
            
            response = helpTable.put_item(
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
    if(method=="createQuestion" ):
        try:
            items = {}
            items["ID"]=uuid.uuid4().hex
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
    if(method=="updateQuestion"):
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
    if(method=="updateHelp"):
        try:
            if(event["arguments"]["input"]["name"] == ""):
                response_data = {
                    "status":204, 
                    "message":"İsim giriniz"
                }
            
                return response_data
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
            response = helpTable.update_item (
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
    if(method=="deleteQuestion"):
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
    if(method=="deleteHelp"):
        try:
            response = helpTable.delete_item(
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
    