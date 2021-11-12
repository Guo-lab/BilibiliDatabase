#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pymysql

# Delete by itself

class Database:
    
    host="127.0.0.1"
    user = "root"
    password=""

    def __init__(self, db):
        connect = pymysql.connect(host=self.host,
                                  user=self.user,
                                  password=self.password,
                                  db=db,
                                  charset='utf8')

        self.cursor = connect.cursor()
        self.con = connect


    def execute(self, command):
        try:
            self.cursor.execute(command)
            self.con.commit()
            

        except Exception as e:
            return e

        else:
            #fetchall() return results, saved as turple
            return self.cursor.fetchall()
            