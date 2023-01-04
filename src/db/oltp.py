from common.dataformat import logger as oltplog
import sqlite3
class DBSqlite(object):
    db_ = None
    def __init__(self, filename):
        self.db_ = sqlite3.connect(filename)

    def createTable(self, sql):
        cursor = self.db_.cursor()
        cursor.exec_(sql)
        cursor.close()
        self.db_.commit()


    def getData(self, sql):
        cursor = self.db_.cursor()
        cursor.exec_(sql)
        result = cursor.fetchall()
        return result
        
    def closeDB(self):
        self.db_.close()

import pymysql
class DBMysql(object):
    db_ = None
    def __init__(self, connect):
        try:
            self.db_ = pymysql.connect(host=connect["host"],port=connect["port"],user=connect["user"],passwd=connect["passward"])
            self.db_.select_db(connect["dbname"])
        except pymysql.err.OperationalError:
            oltplog.error("can not open mysql db!")
        except Exception as err:
            oltplog.error(err)

    def getData(self,sql):
        
        try:
            result = []
            cur =  self.db_.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            oltplog.info(result)      
            return result
        except Exception as err:
            oltplog.error(err)

import pymongo
class DBMongo(object):
    host_ = None
    port_ = None
    client_ = None
    def __init__(self, connect):
        self.host_ = connect["host"]
        self.port_ = connect["port"]
        self.client_ = pymongo.MongoClient(self.host_, self.port_)

    def insertOneData(self, db_name, coll_name, data):
        db = self.client_[db_name]
        coll = db[coll_name]
        result = coll.insert_one(data)
        return result

    def getData(self, db_name, coll_name, condition):
        db = self.client_[db_name]
        coll = db[coll_name]
        result = coll.find_one(condition)
        oltplog.info(result)
        return result
    

        