from  clickhouse_driver import Client
from common.dataformat import logger as olaplog
class DBClickHouse(object):
    client_ = None
    def __init__(self, connect):
        try:
            self.client_ = Client(host=connect["host"],database=connect["db"],user=connect["user"],password=connect["passward"])
        except Exception as err:
            olaplog.error(err)

    def getData(self,sql):
        try:
            result = []
            cur =  self.db_.cursor()
            cur.execute(sql)
            result = cur.fetchall()      
            return result
        except Exception as err:
            olaplog.error(err)
