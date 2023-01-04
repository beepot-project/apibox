from testsuite.basetest import BaseConstructor
from common import rest, EccCrypto
import json
from common.dataformat import logger
import datetime

class TestPeePot(BaseConstructor):
    json_wallet = None
    def setUp(self):
        super().setUp()
        self.loadPrivkey("./ddt/BeePot/privkey.json")
       
    def tearDown(self):
        return super().tearDown()

    def loadPrivkey(self, privkey_file):
        import os 
        self.json_wallet = json.load(open(privkey_file))

    def testBase(self):
        userapi = self.json_config["BeePot"]["userapi"]
        add_user_wallet = "/userWallet/addUserWallet"
        json_add = json.loads("{}")
        json_add["walletAddress"] = "***" #wallet address
        json_add["walletName"] = "autherWallet"
        json_add["userName"] = "autherName"
        json_add["email"] = "test@123.com"
        json_add["source"] = 1
        json_add["hint"] = "testHint"
        json_response = rest.postRequest(userapi, add_user_wallet, json_add)
        code = json_response["code"]
        self.assertEqual(code,'5', "http error")
        
        import datetime
        timestamp = int(datetime.datetime.now().timestamp())
        privkey = self.json_wallet["man_key"]
        login = "/userWallet/login"
        json_login = json.loads("{}")
        json_login["id"] = 1
        json_params  = json.loads("{}")
        json_params["userName"] = EccCrypto.getEccUser(privkey)
        json_login["params"] = json_params
        json_login["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, login, json_login, privkey)
        code = json_response["code"]
        self.assertEqual(code, '200', "http error")

        pubkey = EccCrypto.getEccPubkey(privkey)
        get_ecdh_pubkey = "/userWallet/getEcdhPubKey"
        json_params = json.loads("{}")
        json_params["userPubKey"] = str(pubkey)
        json_params["asset"] = "ETH"
        json_ecdh = json.loads("{}")
        json_ecdh["id"] = 1
        json_ecdh["params"] = json_params
        json_ecdh["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, get_ecdh_pubkey, json_ecdh, privkey)
        code = json_response["code"]
        self.assertEqual(code, '200', "getEcdhPubKey error code: %s"%code)
        json_data = json_response["data"]
        server_pubkey = json_data["serverPubKey"]
        share_aes_key = EccCrypto.getEcdhShareKey(privkey, server_pubkey)
        secret = self.json_wallet["man_key"]
        EccCrypto.aesEnCrypto(share_aes_key, secret)
    
    def formatJsonParam(self, json_file):
        json_params_file  = json.load(open(json_file))
        data = json.dumps(json_params_file["params"]["data"])
        json_params = json.loads("{}")
        json_params["chain"] = json_params_file["params"]["chain"]
        json_params["data"] =  str(data)#
        return json_params

    def formatJsonParamCron(self, json_file):
        json_params_file  = json.load(open(json_file))
        data = json.dumps(json_params_file["params"]["data"])
        json_params = json.loads("{}")
        json_params["taskName"] = json_params_file["params"]["taskName"]
        json_params["chain"] = json_params_file["params"]["chain"]
        json_params["data"] =  str(data)#
        return json_params



    def testAutoCron(self):
        userapi = self.json_config["BeePot"]["userapi"]
        timestamp = 1670822911 #int(datetime.datetime.now().timestamp())
        get_contract_common_config = "/userWallet/getContractCommonConfig"
        privkey = self.json_wallet["owner_key"]
        json_common_config = json.loads("{}")
        json_common_config["id"] = 1
        json_params  = self.formatJsonParam("./ddt/BeePot/getContractCommonConfig.json")
        json_common_config["params"] = json_params
        json_common_config["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, get_contract_common_config, json_common_config, privkey)
        code = json_response["code"]

        get_scheduler_cron = "/userWallet/getSchedulerCron"
        json_cron = json.loads("{}")
        json_cron["id"] = 1
        json_params_cron  = self.formatJsonParamCron("./ddt/BeePot/getSchedulerCronFreshPrice.json")
        json_cron["params"] = json_params_cron
        json_cron["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, get_scheduler_cron, json_cron, privkey)
        code = json_response["code"]

        json_params_cron  = self.formatJsonParamCron("./ddt/BeePot/getSchedulerCronOptionStart.json")
        json_cron["params"] = json_params_cron
        json_cron["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, get_scheduler_cron, json_cron, privkey)
        code = json_response["code"]

        json_params_cron  = self.formatJsonParamCron("./ddt/BeePot/getSchedulerCronAutoBet.json")
        json_cron["params"] = json_params_cron
        json_cron["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, get_scheduler_cron, json_cron, privkey)
        code = json_response["code"]
        
    def testECDH(self):
        userapi = self.json_config["BeePot"]["userapi"]
        mnemonic = self.json_wallet["hd"]
        index = int(datetime.datetime.now().timestamp())
        path = "m/44'/60'/0'/0/" + str(index)
        address,privkey = EccCrypto.getEccHdUser(mnemonic, path)
        
        get_ecdh_pubkey = "/userWallet/getEcdhPubKey"
        timestamp = int(datetime.datetime.now().timestamp())
        pubkey = EccCrypto.getEccPubkey(privkey)
        json_params = json.loads("{}")
        json_params["address"] = address
        json_params["userPubKey"] = str(pubkey).replace("0x","04")
         
        json_ecdh = json.loads("{}")
        json_ecdh["id"] = 1
        json_ecdh["params"] = json_params
        json_ecdh["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, get_ecdh_pubkey, json_ecdh, privkey)
        code = json_response["code"]
        self.assertEqual(code, '200', "getEcdhPubKey error code: %s"%code)
        
        json_data = json_response["data"]
        server_pubkey = json_data["serverPubKey"]
        server_pubkey = server_pubkey[2:]
        share_aes_key = EccCrypto.getEcdhShareKey(privkey, server_pubkey)
        share_aes_key = share_aes_key[32:]
        logger.info("-------------------------------------------")
        logger.info(server_pubkey)
        logger.info(share_aes_key)
    
        secret = privkey
        push_cipher = EccCrypto.aesEnCrypto(share_aes_key, secret)
        logger.info(push_cipher)

        submit_private_key = "/userWallet/submitPrivateKey"
        json_submit = json.loads("{}")
        json_submit["id"] = 1
        json_params  = json.loads("{}")
        json_params["address"] = address
        json_params["privateKey"] = push_cipher
        json_params["userPubKey"] = str(pubkey).replace("0x","04")
        json_params["serverPubKey"] = json_data["serverPubKey"]
        #EccCrypto.getEccUser(privkey)
        json_submit["params"] = json_params
        json_submit["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, submit_private_key, json_submit, privkey)
        code = json_response["code"]
        self.assertEqual(code, '200', "http error")

        json_response = rest.postRequestEcc(userapi, submit_private_key, json_submit, privkey)
        code = json_response["code"]
        self.assertEqual(code, '7', "http error")

        judge_privat_key_exist = "/userWallet/judgePrivateKeyExist"
        json_judge = json.loads("{}")
        json_judge["id"] = 1
        json_params  = json.loads("{}")
        json_params["address"] = address#EccCrypto.getEccUser(privkey)
        json_judge["params"] = json_params
        json_judge["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, judge_privat_key_exist, json_judge, privkey)
        code = json_response["code"]
        self.assertEqual(code, '200', "http error")


    def testgetSchedulerCron(self):
        userapi = self.json_config["BeePot"]["userapi"]
        timestamp = int(datetime.datetime.now().timestamp())
        privkey = self.json_wallet["owner_key"]
        login = "/userWallet/getSchedulerCron"
        json_login = json.loads("{}")
        json_login["id"] = 1
        json_params  = json.load(open("./ddt/BeePot/getSchedulerCron.json"))
        json_params["userName"] = EccCrypto.getEccUser(privkey)
        json_login["params"] = json_params
        json_login["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, login, json_login, privkey)
        code = json_response["code"]
        

    def testAddUserWallet(self):
        userapi = self.json_config["BeePot"]["userapi"]
        add_user_wallet = "/userWallet/addUserWallet"
        mnemonic = self.json_wallet["hd"]
        index = int(datetime.datetime.now().timestamp())
        path = "m/44'/60'/0'/0/" + str(index)
        address,privkey = EccCrypto.getEccHdUser(mnemonic, path)
        # check new addres is ok!
        json_add = json.loads("{}")
        json_add["walletAddress"] = str(address)
        json_add["walletName"] = "autherWallet" + str(index)
        json_add["userName"] = "autherName" + str(index)
        json_add["email"] = "test%d@123.com"%index
        json_add["source"] = 1
        json_add["hint"] = "testHint"
        
        json_response = rest.postRequest(userapi, add_user_wallet, json_add)
        code = json_response["code"]
        self.assertEqual(code,'200', "addUserWallet error code %s"%code)

        # check reset addres is ok!
        json_response = rest.postRequest(userapi, add_user_wallet, json_add)
        code = json_response["code"]
        self.assertEqual(code,'5', "addUserWallet error code %s"%code)
        
        # check not set email addres is ok!
        index = index + 1
        path = "m/44'/60'/0'/0/" + str(index)
        address,privkey = EccCrypto.getEccHdUser(mnemonic, path)
        json_add["walletAddress"] = str(address)
        json_add["walletName"] = "autherWallet" + str(index)
        json_add["userName"] = "autherName" + str(index)
        #json_add["email"] = "test%d123.com"%index
        json_add["source"] = 1
        json_add["hint"] = "testHint"
        
        json_response = rest.postRequest(userapi, add_user_wallet, json_add)
        code = json_response["code"]
        self.assertEqual(code,'200', "addUserWallet error code %s"%code)

        # check error address is ok!
        json_add["walletAddress"] = "error address"
        json_add["walletName"] = "autherWallet" + str(index)
        json_add["userName"] = "autherName" + str(index)
        #json_add["email"] = "test%d123.com"%index
        json_add["source"] = 1
        json_add["hint"] = "testHint"
        
        json_response = rest.postRequest(userapi, add_user_wallet, json_add)
        code = json_response["code"]
        self.assertEqual(code,'3', "addUserWallet error code %s"%code)

    def testLogin(self):
        # check normal user login is ok !
        import datetime
        timestamp = int(datetime.datetime.now().timestamp())
        privkey = "***"
        login = "/userWallet/login"
        userapi = self.json_config["BeePot"]["userapi"]
        json_login = json.loads("{}")
        json_login["id"] = 1
        json_params  = json.loads("{}")
        json_params["userName"] = EccCrypto.getEccUser(privkey)
        json_login["params"] = json_params
        json_login["timestamps"] = timestamp
        json_response = rest.postRequestEcc(userapi, login, json_login, privkey)
        code = json_response["code"]
        self.assertEqual(code, '200', "http error")

        # check not register user login is ok!
        index = int(datetime.datetime.now().timestamp())
        path = "m/44'/60'/0'/0/" + str(index)
        mnemonic = self.json_wallet["hd"]
        address,privkey = EccCrypto.getEccHdUser(mnemonic, path)
        json_params["userName"] = address
        json_response = rest.postRequestEcc(userapi, login, json_login, privkey)
        code = json_response["code"]
        self.assertEqual(code, '200', "http error")
       


        










        
   
    
