import json
import boto3
import uuid

import sys
from boto3.dynamodb.conditions import Key,Attr

def lambda_handler(event, context):
    tableName = "shelveTable"
    bookcaseName="bookcaseTable"
    cellName = "cellTable"
    bookName= "bookTable" 
    
    client = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    
    table = DB.Table(tableName)
    bookcaseTable= DB.Table(bookcaseName)
    cellTable= DB.Table(cellName)
    bookTable= DB.Table(bookName)
    
    method = event["info"]["fieldName"]
    cognito_sub= event["identity"]["sub"]
    if(method=="getShelveCell"):
        try:
            response=cellTable.scan(
                FilterExpression = Attr("shelveId").eq(str(event["arguments"]["ID"]))
            )
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
    if(method=="searchAllShelves"):
        try:
            if("name" in event["arguments"] and event["arguments"]["name"] != ""):
                print("a")
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
            if("limit" in event["arguments"] and  event["arguments"]!= ""):
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
    
    if(method== "getShelve"):
        try:
            Primary_Column_Name = "ID"
            Primary_Key = event["arguments"]["ID"]
            if(Primary_Key == ""):
                response = {
                    "ID":""
                }
                return response 
            response = table.get_item(
                Key={
                    Primary_Column_Name:Primary_Key
                }
            )
            print(response)
            if("Item" not in response):
                response = {
                    "ID":""
                }
                return response 
            return response["Item"]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response
        
    
    if(method == "createShelve"):
        try:
            if("bookcaseId" in event["arguments"]["input"] and  event["arguments"]["input"]["bookcaseId"] == ""):
                response_data = {
                    "status":204, 
                    "message":"bookcaseId giriniz"
                }
                
                return response_data
            items = {}
            for key,value in event["arguments"]["input"].items():
                items[key] = value
            items["ID"]=str(uuid.uuid4())
            items["userId"]=cognito_sub
            getbookcase = bookcaseTable.scan(
                FilterExpression = Attr("Id").eq(items["bookcaseId"])
            ) 
            print(getbookcase["Items"])
            number =getbookcase["Items"][0]["shelvesNumber"]+1
            bookcaseUpdate = bookcaseTable.update_item(
                Key={
                    "Id":str(event["arguments"]["input"]["bookcaseId"]),
                },
                UpdateExpression= 'SET #shelvesNumber = :shelvesNumber',
                ExpressionAttributeNames={
                    "#shelvesNumber":"shelvesNumber"
                },
                ExpressionAttributeValues = {
                    ":shelvesNumber":number,
                }
            )
            
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
            print('Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response
    Primary_Column_Name = "ID"
    Primary_Key = event["arguments"]["input"]["ID"]  
    if(method == "deleteShelve"):
        try:
            shelve = table.get_item(
                Key={
                    Primary_Column_Name:Primary_Key
                }
            )
            bookcase = bookcaseTable.get_item(
                Key={
                    "Id":shelve["Item"]["bookcaseId"]
                }
            )
            updateBookcase = bookcaseTable.update_item(
                Key={
                    "Id": shelve["Item"]["bookcaseId"]
                },
                UpdateExpression= 'SET #shelvesNumber= :shelvesNumber',
                ExpressionAttributeNames={
                    "#shelvesNumber":"shelvesNumber"
                },
                ExpressionAttributeValues = {
                    ":shelvesNumber" :bookcase["Item"]["shelvesNumber"]-1
                }
            )
            response = table.delete_item(
                Key={
                    Primary_Column_Name:Primary_Key
                }
            )
            
            deleteCell = cellTable.scan(
                FilterExpression = Attr("shelveId").eq(event["arguments"]["input"]["ID"])
            )
            for value in deleteCell["Items"]:
                response = cellTable.delete_item(
                    Key={
                        "ID":str(value["ID"])
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
            print('Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno))
            response = {
                "status":"204",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response
    if(method == "updateShelve"):
        try:
            response = table.update_item (
                Key={
                    Primary_Column_Name:Primary_Key
                },
                UpdateExpression= 'SET #name = :name',
                ExpressionAttributeNames={
                    "#name":"name"
                },
                ExpressionAttributeValues ={
                    ":name":event["arguments"]["input"]["name"]
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
            print('Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response