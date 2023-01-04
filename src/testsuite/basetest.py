import unittest
class BaseConstructor(unittest.TestCase):
    json_config = None
    def setUp(self):
        self.resetConfig("./config/config.json")
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
    def resetConfig(self, file):
        import os 
        import json
        self.json_config = json.load(open(file))



   