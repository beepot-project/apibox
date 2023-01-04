
class ApiCompareBasic(object):
    api_dict_ = {}
    basic_dict_ = {}
    project_ = None
    def __init__(self, project:str):
        self.project_ = project        
   
    def getApiData(self,name:str):
        api_data = self.api_dict_[name]
        return api_data
        
    def getBasicData(self, name:str):
        basic_data = self.api_dict_[name]
        return basic_data

    def setApiData(self, key: str, value):
        self.api_dict_[key] = value

    def setBasicData(self, key: str, value):
        self.basic_dict_[key] = value
