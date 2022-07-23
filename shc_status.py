from requests import get
import json
import time
import boto3
import os
from base64 import b64decode

splunk_user = os.environ['SPLUNK_USER']
splunk_secret = os.environ['SPLUNK_SECRET']
splunk_pem = os.environ['SPLUNK_PEM']
splunk_url = os.environ['SPLUNK_URL']

splunk_password = boto3.client('kms').decrypt(CiphertextBlob=b64decode(splunk_secret))['Plaintext']


def call_splunk_api(retries = 0):
    try: 
        
        response = get(splunk_url, verify=splunk_pem,  auth=(splunk_user, splunk_password))
        print(response)
        #print(response.json())
        json_str = response.json()

        #print('-------------------------------------')
        #print(json.dumps(json_str, indent=4))
        pretty_json=json.dumps(json_str, indent=4)
        #print(pretty_json)
        sampleDict=json.loads(pretty_json)

        #print(sampleDict)
        #print('-------------------------------------')
        return sampleDict

    except: 
        retries += 1
        print("Sleeping for 5 sec, will try restAPI call again")
        time.sleep(1)
        print(retries)
        if retries < 3:
            call_splunk_api(retries)
            print("Cannot connect to Search head cluster")

        
def get_shc_status():

    try: 
        json_return = call_splunk_api()
        
        my_status = []
        print(json_return)
        for value in json_return['entry'][0]['content']['peers']:
            #print(value)

            #print(json_return['entry'][0]['content']['peers'][value]['status'])
            
            my_status.append(json_return['entry'][0]['content']['peers'][value]['status'])
            
            #print(my_status)
        return my_status
            

    except Exception as e:
        print("Exception is :" + str(e) )


def shc_status_check():
    i = 0
    res = []
    my_status = get_shc_status()
    for x in my_status:
        #print(x)
        if x == 'Up':
            print("SHC member is : " +x)
        else:
            res.append(x)
    return res
        
    return x

def lambda_handler(event, context):
    status =  shc_status_check()
    return status
 




