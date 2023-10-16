import json
import boto3
import uuid
import sys
from boto3.dynamodb.conditions import Key,Attr

def lambda_handler(event, context):
    tableName="bookcaseTable"
    shelveTableName = "shelveTable"
    tablename="cellTable"
    bookName="bookTable"
        
    
    client = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    
    table = DB.Table(tableName)
    shelveTable = DB.Table(shelveTableName)
    cellTable= DB.Table(tablename)
    bookTable = DB.Table(bookName)
    
    method = event["info"]["fieldName"]
    cognito_sub= event["identity"]["sub"]
    

    if(method=="allBookcaseItem"):
        try:
            getShelves=shelveTable.scan(
                FilterExpression = Attr("bookcaseId").eq(event["arguments"]["Id"])
            )
            for value in getShelves["Items"]:
                getCells = cellTable.scan(
                    FilterExpression = Attr("shelveId").eq(str(value["ID"]))
                )
                value["cell"] = getCells["Items"]
                for value in getCells["Items"]:
                    getBook = bookTable.scan(
                        FilterExpression = Attr("ID").eq(value["bookId"][0])
                    )
                    if(getBook["Items"] != []):
                        value["book"]=getBook["Items"][0]["image"]
                    else:
                        value["book"]=""
            return getShelves["Items"]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response
    if(method=="getBookcaseShelve"):
        try:
            response= shelveTable.scan(
                FilterExpression = Attr("bookcaseId").eq(str(event["arguments"]["Id"]))
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
    if(method=="searchAllBookcase"):
        try:
            if("name" in event["arguments"] and "name" != ""):
                if("LastEvaluatedKey" in event["arguments"] and event["arguments"]["LastEvaluatedKey"] != ""):
                    a = {}
                    a["Id"]=event["arguments"]["LastEvaluatedKey"]
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
                    a["Id"]=event["arguments"]["LastEvaluatedKey"]
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
    if(method == "getBookcase"):
        try:
            Primary_Column_Name = "Id"
            Primary_Key = event["arguments"]["Id"]
            response = table.get_item(
                Key={
                    Primary_Column_Name:Primary_Key
                }
            )
            print(response)
            if("Item" in response):
                return response["Item"]
            else:
                return {"Id":""}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(e, exc_type, exc_tb.tb_lineno)
            }
            return response
        
        
    if(method== "createBookcase"):
        try:
            items = {}
            for key,value in event["arguments"]["input"].items():
                items[key] = value
            items["Id"] = str(uuid.uuid4())
            items["userId"]=cognito_sub
            response = table.put_item(
                Item = items
            )
            shelve = shelveTable.scan()
            count = 0
            while count < event["arguments"]["input"]["shelvesNumber"]:
                count += 1
                shelves = shelveTable.put_item(
                    Item = {
                        "ID" :str(uuid.uuid4()),
                        "bookcaseId" : items["Id"],
                        "userId":cognito_sub
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
    Primary_Column_Name = "Id"
    Primary_Key = event["arguments"]["input"]["Id"]
    
    if(method=="updateBookcase"):
        try:   
            ExpressionAttributes = {}
            test = {}
            strValues = ""
            if("shelvesNumber" in event["arguments"]["input"]):
                
                getShelveNumber = table.get_item(
                    Key={
                        Primary_Column_Name:Primary_Key
                    },
                )
                if(getShelveNumber["Item"]["shelvesNumber"] >= event["arguments"]["input"]["shelvesNumber"]):
                    message = {
                        "status":getShelveNumber["ResponseMetadata"]["HTTPStatusCode"], 
                        "message":"Raf sayısı mevcut sayıdan daha fazla olmalıdır"
                    }
                
                    return message
                shelve = shelveTable.scan()
                count = getShelveNumber["Item"]["shelvesNumber"]
                newCount = event["arguments"]["input"]["shelvesNumber"]
                while count < newCount:
                    count += 1
                    shelves = shelveTable.put_item(
                        Item = {
                            "ID" :str(uuid.uuid4()),
                            "bookcaseId" : Primary_Key,
                            "userId":cognito_sub
                        }
                    )
            
            for key,value in event["arguments"]["input"].items():
                if(key != "Id"):
                    data_name = ":"+key
                    data_name2 = "#"+key
                    ExpressionAttributes[data_name] = value
                    test[data_name2] = key
                    strValues += "#"+key+"=:"+key+","
                    
            strValues = strValues[:len(strValues)-1]
            response = table.update_item (
                Key={
                    Primary_Column_Name:Primary_Key
                },
                UpdateExpression= 'SET '+strValues,
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
    if(method== "deleteBookcase"):
        try:
            deleteCells = cellTable.scan(
                FilterExpression = Attr("bookcaseId").eq(str(event["arguments"]["input"]["Id"]))
            )
            
            for value in deleteCells["Items"]:
                response = cellTable.delete_item(
                    Key={
                        "ID":str(value["ID"])
                    }
                )
            
            deleteShelves = shelveTable.scan(
                FilterExpression = Attr("bookcaseId").eq(Primary_Key)
            )
            for value in deleteShelves["Items"]:
                response = shelveTable.delete_item(
                    Key={
                        "ID":str(value["ID"])
                    }
                )
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