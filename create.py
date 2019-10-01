
import json
import logging
import os
import time
import uuid
from apis import decimalencoder
import boto3
from flask import Flask, jsonify, request,Response
from apis.sendNotification import send_notification
from apis.sendNotification import send_email
import stripe

res = boto3.setup_default_session(region_name='us-east-1')
dynamodb = boto3.resource('dynamodb')
client = boto3.client('cognito-idp')
pin = boto3.client('pinpoint')

def add(entityName):
    data = request.json
    timestamp = int(time.time() * 1000)
    table = dynamodb.Table(os.environ[entityName])
    print("------------Start-------")
    print("Create "+entityName+" data")
    try:
        item=data['entityData']
        item["id"]= item["id"] if 'id' in item else str(uuid.uuid1())
        item["createdAt"] = timestamp
        item["updatedAt"] = timestamp
        res = table.put_item(Item=item)
        print("-------End-----------")
        return Response(json.dumps(item), status=200, mimetype='application/json')
    except Exception as e:
        body = e.json_body
        err  = body.get('error', {})
        print("---------------Error Start----------")
        print(err)
        print("---------------Error End------------")
        return Response(json.dumps({"message":err.get('message'),"statusCode":1}), status=500,mimetype='application/json')
        pass


def addDeviceToken():
    data = request.json
    timestamp = int(time.time() * 1000)
    table = dynamodb.Table(os.environ["deviceTokens"])
    print("------------Start-------")
    print("Create deviceToken data")

    result = table.scan(
        FilterExpression= "deviceToken = :deviceToken",
        ExpressionAttributeValues= {
                ":deviceToken" : data['entityData']['deviceToken']
        }
    )
    if(len(result['Items']) == 0):
        try:
            item=data['entityData']
            item["id"]= str(uuid.uuid1())
            item["createdAt"] = timestamp
            item["updatedAt"] = timestamp
            item["statusCode"] = 1
            res = table.put_item(Item=item)
            print("-----------End-----------")
            return Response(json.dumps(item), status=200, mimetype='application/json')
        except Exception as e:
            body = e.json_body
            err  = body.get('error', {})
            print("---------------Error Start----------")
            print(err)
            print("---------------Error End------------")
            return Response(json.dumps({"message":err.get('message'),"statusCode":1}), status=500,mimetype='application/json')
            pass
    else:
        print("-----------End-----------")
        return Response(json.dumps({"message":"This device token already exists","statusCode":1}), status=200, mimetype='application/json')

def addUser():
    data = request.json
    timestamp = int(time.time() * 1000)
    userTable = dynamodb.Table(os.environ["users"])
    print("------------Start-------")
    print("Create user data")
    try:
        item=data['entityData']
        item["id"]= item["id"]
        item["createdAt"] = timestamp
        item["updatedAt"] = timestamp
        
        # Link user and organization
        orgUserTable = dynamodb.Table(os.environ["organizationUsers"])
        userData = {}
        userData["id"] = str(uuid.uuid1())
        userData["orgId"] = item["orgId"]
        userData["userId"] = item["id"]
        userData["createdAt"] = timestamp
        userData["updatedAt"] = timestamp
        
        # Assign scripts and questions in a Care Giver user
        if (item["userProfile"] == "C"):
            scriptTable = dynamodb.Table(os.environ["orgScripts"])
            scriptResult = scriptTable.scan(
                IndexName = "orgId-index",
                FilterExpression= "orgId = :orgId",
                ExpressionAttributeValues= {
                    ":orgId" : item["orgId"]
                }
            )
            res = saveScriptsAndQuestions(scriptResult["Items"],item["orgId"],"userScripts","userQuestions",item['firstName'],item["id"])
            if res["statusCode"] == 1:
                return Response(json.dumps({"message":res["message"],"statusCode":1}), status=500,mimetype='application/json')
            else:
                res = userTable.put_item(Item=item)
                orgUserTable.put_item(Item=userData)

        print("-------End-----------")
        return Response(json.dumps(item), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message":e,"statusCode":1}), status=500,mimetype='application/json')
        pass

def userProfile():
    data = request.json
    timestamp = int(time.time() * 1000)
    updateUserTable = dynamodb.Table(os.environ["userProfile"])
    print("------------Start-------")
    try:
        item=data['entityData']
        item["id"]= item["id"]
        item["createdAt"] = timestamp

        userContact={}
        userContact["id"]=str(uuid.uuid1())
        userContact["PrimaryMobile"]= item[primaryMobile]
        userContact["address"]= item[address]
        userContact["city"]= item[city]
        userContact["state"]= item[state]
        userContact["country"]= item[country]
        userContact["postCode"]= item[postCode]




    
    


def createOrg():
    data = request.json
    timestamp = int(time.time() * 1000)
    table = dynamodb.Table(os.environ["organizations"])
    print("------------Start-------")
    print("Create organization")
    try:
        item=data['entityData']
        item["id"]= str(uuid.uuid1())
        item["createdAt"] = timestamp
        item["updatedAt"] = timestamp

        scriptTable = dynamodb.Table(os.environ["orgScripts"])
        scriptResult = scriptTable.scan(
            ScanFilter= {
                "id": {
                    "ComparisonOperator": "IN",
                    "AttributeValueList": item["scripts"].split(",")
                }
            }
        )
        # Assign scripts and questions to a organization
        res = saveScriptsAndQuestions(scriptResult["Items"],item["id"],"orgScripts","orgQuestions",item['orgName'],'')
        if res["statusCode"] == 1:
            return Response(json.dumps({"message":res["message"],"statusCode":1}), status=500,mimetype='application/json')
        else:
            # Create the organization
            res = table.put_item(Item=item)
        
        print("-------End-----------")
        return Response(json.dumps(item), status=200, mimetype='application/json')
    except Exception as e:
        body = e.json_body
        err  = body.get('error', {})
        print("---------------Error Start----------")
        print(err)
        print("---------------Error End------------")
        return Response(json.dumps({"message":err.get('message'),"statusCode":1}), status=500,mimetype='application/json')
        pass


def saveScriptsAndQuestions(scripts,orgId,scriptSaveTable,questionsSaveTable,assignTo,userId):
    
    try:
        timestamp = int(time.time() * 1000)
        scriptTable = dynamodb.Table(os.environ["orgScripts"])
        questionIds = set()

        # Read the all questions from scripts
        for script in scripts:
            for category in script["questions"].keys():
                for  question in script["questions"][category]:
                    questionIds.add(question['id'])

        # Read all questions data from global organization
        questionTable = dynamodb.Table(os.environ["orgQuestions"])
        questionResult = questionTable.scan(
            ScanFilter= {
                "id": {
                    "ComparisonOperator": "IN",
                    "AttributeValueList": list(questionIds)
                }
            }
        )

        #Save the questions to created organization
        questionSave = dynamodb.Table(os.environ[questionsSaveTable])
        print("Questions saving start")
        newQuestionIds = {}
        for question in questionResult['Items']:
            question['linkId'] = question['id']
            question['id'] = str(uuid.uuid1())
            question['orgId'] = orgId
            if userId != "":
                question['userId'] = userId
            question["createdAt"] = timestamp
            question["updatedAt"] = timestamp
            newQuestionIds[question['linkId']] = question['id']
            questionSave.put_item(Item=question)
        print("Questions saved to "+assignTo)

        # Change the question ids in script and save the script
        scriptSave = dynamodb.Table(os.environ[scriptSaveTable])
        print("Scripts saving start")
        for script in scripts:
            for category in script["questions"].keys():
                for  question in script["questions"][category]:
                    question['id'] = newQuestionIds[question['id']]
            script['linkId'] = script['id']
            script['id'] = str(uuid.uuid1())
            script['orgId'] = orgId
            if userId != "":
                script['userId'] = userId
            script["createdAt"] = timestamp
            script["updatedAt"] = timestamp
            scriptSave.put_item(Item=script)
        print("Scripts saved to "+assignTo)
        return ({"message":"success","statusCode":0})
    except Exception as e:
        print(e)
        return ({"message":e,"statusCode":1})
        pass
