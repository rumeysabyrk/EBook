import json
import boto3
import datetime
import uuid
import sys
from boto3.dynamodb.conditions import Key,Attr

def lambda_handler(event, context):
    tableName="userTable"
    shelveTableName = "shelveTable"
    cellName="cellTable"
    bookName="bookTable"
    bookcaseName="bookcaseTable"
        
    client = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    
    table = DB.Table(tableName)
    shelveTable = DB.Table(shelveTableName)
    cellTable= DB.Table(cellName)
    bookTable = DB.Table(bookName)
    bookcaseTable=DB.Table(bookcaseName)
    
    method = event["info"]["fieldName"]
    cognito_sub= event["identity"]["sub"]
    if(method=="getUserBookcase"):
        try:
            response = bookcaseTable.scan(
                FilterExpression = Attr("userId").eq(cognito_sub)
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
    if(method == "getUser"):
        try:
            response = table.get_item(
                Key={
                    "ID":cognito_sub
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
    
    if(method== "listUsers"):
        try:
            if("LastEvaluatedKey" in event["arguments"] and event["arguments"]["LastEvaluatedKey"] != "" ):
                a = {}
                a["ID"]=event["arguments"]["LastEvaluatedKey"]
                response = table.scan(
                    Limit=event["arguments"]["limit"],
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
    
    if(method == "createUser"):
        try:
            items = {}
            for key,value in event["arguments"]["input"].items():
                items[key] = value
            items["ID"]=cognito_sub
            items["createdAt"]=str(datetime.datetime.now())
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
    if(method == "updateUser"):
        try:
            findUser = table.get_item(
                Key={
                    "ID":cognito_sub
                }
            )
            if("Item" not in findUser):
                response_data = {
                    "status":404, 
                    "message":"Kullanıcı bulunamadı"
                }
                
                return response_data   
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
            
            strValues += "#updatedAt = :updatedAt"
            test["#updatedAt"] = "updatedAt"
            ExpressionAttributes[":updatedAt"] = str(datetime.datetime.now())
            response = table.update_item (
                Key={
                    "ID":cognito_sub
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
    if(method == "deleteUser"):
        try:
            findUser = table.get_item(
                Key={
                    "ID":cognito_sub
                }
            )
            if("Item" not in findUser):
                response_data = {
                    "status":404, 
                    "message":"Kullanıcı bulunamadı"
                }
                
                return response_data   
            response = table.delete_item(
                Key={
                    "ID":cognito_sub
                }
            )
            deleteCells = cellTable.scan(
                FilterExpression = Attr("userId").eq(cognito_sub)
            )
            
            for value in deleteCells["Items"]:
                response = cellTable.delete_item(
                    Key={
                        "ID":str(value["ID"])
                    }
                )
            
            deleteBookcase = bookcaseTable.scan(
                FilterExpression = Attr("userId").eq(cognito_sub)
            )
            
            for value in deleteBookcase["Items"]:
                response = bookcaseTable.delete_item(
                    Key={
                        "Id":str(value["Id"])
                    }
                )
            
            deleteShelves = shelveTable.scan(
                FilterExpression = Attr("userId").eq(cognito_sub)
            )
            for value in deleteShelves["Items"]:
                response = shelveTable.delete_item(
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
                "status":"500",
                "message":'Error: {} - {}  - {}'.format(str(e), exc_type, exc_tb.tb_lineno)
            }
            return response
            
    if(method=="createSomething"):
        cognito_client = boto3.client('cognito-idp', region_name='eu-north-1')

        # Parola değişikliğini zorlamak istediğiniz kullanıcının kimlik bilgilerini belirtin
        username = '9df24705-f687-42c3-b6b1-223ccf397ffb'
        user_pool_id = 'eu-north-1_Ah2AlpfDv'
    
        # Parola değişikliğini zorlama isteğini gönderin
        response = cognito_client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password='Rb369852*',
            Permanent=True  # Bu, kullanıcının parolasının kalıcı olarak değiştirilmesini sağlar
        )
    
        # Yanıtı işleyin ve işlem sonucunu kontrol edin
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return "Parola değişikliği başarıyla zorlandı."
        else:
            return "Parola değişikliği zorlanırken bir hata oluştu."
