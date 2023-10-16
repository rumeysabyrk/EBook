import json
import boto3
import uuid
import sys
from boto3.dynamodb.conditions import Key,Attr

def lambda_handler(event, context):
    tableName = "cellTable"
    bookName= "bookTable" 
    
    client = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    
    table = DB.Table(tableName)
    bookTable= DB.Table(bookName)
    
    method = event["info"]["fieldName"]
    cognito_sub= event["identity"]["sub"]
    if(method == "deleteCellBook"):
        try:
            cell = table.get_item(
                Key = {
                    "ID":event["arguments"]["cellId"]
                }
            )
            items= cell["Item"]["bookId"]
            for value in cell["Item"]["bookId"]:
                if(value == event["arguments"]["ID"]):
                    items.remove(value)
                    response = table.update_item(
                        Key = {
                            "ID":event["arguments"]["cellId"]
                        },
                        UpdateExpression= 'SET #bookId = :bookId',
                        ExpressionAttributeNames={"#bookId":"bookId"},
                        ExpressionAttributeValues = {":bookId":items}
                    )
                        
                    
                    response_data = {
                        "status":response["ResponseMetadata"]["HTTPStatusCode"], 
                        "message":"Başarılı"
                    }
                    
                    return response_data
                else:
                    response_data = {
                        "status":404, 
                        "message":"Silmek istediğiniz kitap bu hücrede mevcut değil"
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
    if(method=="scanGroup"):
        try:
            
            items=[]
            for value in event["arguments"]["ISBN"]:
                getBook = bookTable.scan(
                    FilterExpression = Attr("ISBN").eq(value)
                )
                items.append(getBook["Items"][0]["ID"])
            response = table.update_item(
                Key = {
                    "ID":event["arguments"]["cellId"]
                },
                UpdateExpression= 'SET #bookId = :bookId',
                ExpressionAttributeNames={"#bookId":"bookId"},
                ExpressionAttributeValues = {":bookId":items}
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
            
    if(method =="addCellBook"):
        try:
            cell = table.get_item(
                Key={
                    "ID":event["arguments"]["cellId"]
                }
            )
            for value in cell["Item"]["bookId"]:
                if(value == event["arguments"]["ID"]):
                    response_data = {
                        "status":204, 
                        "message":"Eklemek istediğiniz kitap hücrenizde mevcut"
                    }
                    
                    return response_data
            items=[]
            books= table.get_item(
                Key={
                    "ID":event["arguments"]["cellId"]
                }
            )
            items=books["Item"]["bookId"]
            items.append(event["arguments"]["ID"])
            response = table.update_item(
                Key={
                    "ID":event["arguments"]["cellId"]
                },
                UpdateExpression= 'SET #bookId = :bookId',
                ExpressionAttributeNames={"#bookId":"bookId"},
                ExpressionAttributeValues = {":bookId":items}
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
    if(method=="deleteCells"):
        try:
            for value in event["arguments"]["ID"]:
                response = table.delete_item(
                    Key={
                        "ID":str(value)
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
            
            
            
    if(method=="getCellBook"):
        try:
            Items=[]
            cell= table.get_item(
                Key = {
                    "ID":event["arguments"]["ID"]
                }
            )
            for value in cell["Item"]["bookId"]:
                response = bookTable.get_item(
                    Key = {
                        "ID":value
                    }
                )
                Items.append(response["Item"])
            return Items
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(sys.exc_info())
            print('Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response
    if(method=="moveCell"):
        try:
            for value in event["arguments"]["input"]["ID"]:
                
                response = table.update_item(
                    Key={
                        "ID":str(value)
                    },
                    UpdateExpression= 'SET #shelveId = :shelveId',
                    ExpressionAttributeNames={"#shelveId":"shelveId"},
                    ExpressionAttributeValues = {":shelveId":event["arguments"]["input"]["shelveId"]}
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
        
        
        
    if(method== "listCells"):
        try:
            if("LastEvaluatedKey" in event["arguments"] and event["arguments"]["LastEvaluatedKey"] !=""):
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
            print('Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response
        
    if(method== "getCell"):
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
            print('Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response
    
    if(method == "createCell"):
        try:
            if(event["arguments"]["input"]["bookcaseId"] == "" or event["arguments"]["input"]["shelveId"] == ""):
                response_data = {
                    "status":204, 
                    "message":"Id giriniz"
                }
                
                return response_data
            items = {}
            items["userId"]=cognito_sub
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
            print('Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response
    Primary_Column_Name = "ID"
    Primary_Key = event["arguments"]["input"]["ID"]
    
    
    if(method=="updateCell"):
        try:
            ExpressionAttributes = {}
            test = {}
            strValues = ""
            for key,value in event["arguments"]["input"].items():
                if(key != "ID"):
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
            print('Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response
            
            
            
    if(method == "deleteCell"):
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
            print('Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno))
            response = {
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response