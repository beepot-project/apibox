#!/usr/bin/python3

import requests
from common.dataformat import logger as relog
import json

def getRequest(url, interface, params, headers):
    relog.info("\n \nFunction getRequest(url, interface, params, headers)")
    try:
        relog.info(url + interface)
        interface_url = url + interface
        relog.info(params)
        relog.info(headers)
        res = requests.get(url=interface_url, params=params, headers=headers)
        json_response = json.loads(res.content)
        return json_response
    except Exception as err:
        relog.error(err)

def postRequest(url, interface, json_post):
    relog.info("\n \npostRequest(url, interface, json_post)")
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    try:
        relog.info("http Post url : ")
        relog.info(url + interface)
        interface_url = url + interface
        relog.info("Post data : ")
        relog.info(json.dumps(json_post))
        relog.info("http headers : ")
        relog.info(headers)
        res = requests.post(url=interface_url, data=json.dumps(json_post), headers=headers)
        json_response = json.loads(res.content)
        relog.info("http response : ")
        relog.info(res.content)
        return json_response
    except Exception as err:
        relog.error(err)

def postRequestEcc(url, interface, json_post, privkey):
    from common import EccCrypto
    relog.info("\n \nFunction postRequestEcc(url, interface, json_post, headers, privkey)")
    relog.info("http Post url: ")
    relog.info(url + interface)
    relog.info("Post data : ")
    relog.info(json.dumps(json_post))
    
    params = json.dumps(json_post["params"]).replace(' ', '')
    #params = params.replace('\\\"', '\"')
    timestamps = json_post['timestamps']
    msg = url.replace('https', 'http') + interface + params + str(timestamps)
    signed_msg,address = EccCrypto.signMessage(msg, privkey)
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    headers["author"] = address
    headers["signer"] = signed_msg
    relog.info("http headers : ")
    relog.info(headers)
    try:
        interface_url = url + interface
        res = requests.post(url=interface_url, data=json.dumps(json_post).replace(' ', ''), headers=headers)
        json_response = json.loads(res.content)
        relog.info("http response : ")
        relog.info(res.content)
        return json_response
    except Exception as err:
        relog.error(err)