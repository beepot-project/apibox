
class ApiCompareDb(object):
    api_dict_ = {}
    dbmysql_connect_ = {}
    dbmongodb_connect_ = {}

    project_ = None
    def __init__(self, project:str):
        self.project_ = project        
   
    def getApiData(self,name:str):
        api_data = self.api_dict_[name]
        return api_data

    def setApiData(self, key: str, value):
        self.api_dict_[key] = value

