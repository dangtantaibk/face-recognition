import sqlite3
class DataProvider:
    databaseName = "./database/human_resources.db";
    def __init__(self):
        return;
    def execute(self,sql,params_tuple = ()):
        con = sqlite3.connect(self.databaseName)
        try:
            cur = con.cursor()
            cur.execute(sql,params_tuple)
            con.commit();
            cur.close();
            con.close();
        except Exception as err:
            if con:
                con.close()
            print(f"Unexpected {err=}, {type(err)=}")
       
    def fetchall(self,sql):
        con = sqlite3.connect(self.databaseName)
        try:
            cur = con.cursor()
            res = cur.execute(sql)
            result = res.fetchall();
            cur.close();
            con.close();
            return result;
        except Exception as err:
            if con:
                con.close()
            print(f"Unexpected fetchall {err=}, {type(err)=}")
            return None;

        
        