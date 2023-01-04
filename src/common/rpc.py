#!/usr/bin/python3

import requests
from common.dataformat import logger as rpclog
import json
def doJsonRpc(url, method, params, headers):
    try:
        rpc_data = {}
        rpc_data["method"] = method
        rpc_data["params"] = params
        res = requests.post(url=url, data=json.dumps(rpc_data), headers=headers)
        json_response = json.loads(res.content)
        return json_response
    except Exception as err:
        rpclog.error(err)
