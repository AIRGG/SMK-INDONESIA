import pymysql
import pandas as pd


class Database:
    """docstring for database"""

    def __init__(self):
        # super(database, self).__init__()
        host = "127.0.0.1"
        user = "root"
        pswd = ""
        db = "smkindonesia"

        self.con = pymysql.connect(
            host=host, user=user, password=pswd, db=db, cursorclass=pymysql.cursors.DictCursor)

        self.cur = self.con.cursor()

    def getData(self, sql, stmt=False, df=False):
        # connection = self.getConnection()
        # try:
        # 	crsr = connection.cursor()
        # 	if(stmt == False):
        # 		crsr.execute(sql)
        # 	else:
        # 		crsr.execute(sql, stmt)
        # except Exception as e:
        # 	raise e
        # finally:
        # 	connection.close()

        result = None
        try:

            if stmt == False:
                print("Melakukan Eksekusi SQL: "+sql)
                # self.cur.execute(sql)
                result = pd.read_sql(sql, self.con)

            else:
                print("Melakukan Eksekusi SQL: "+sql, stmt)
                result = pd.read_sql(sql, self.con, params=stmt)

        except Exception as e:
            print(e)
            return 0
        if df:
            return result
        else:
            result = result.to_json(orient="records")
        # result = self.toJSON(self.cur.fetchall())
        return result

    def execSql(self, sql, stmt=False):
        try:
            if stmt == False:
                print("Melakukan Eksekusi SQL: "+sql)
                self.cur.execute(sql)
            else:
                print("Melakukan Eksekusi SQL: "+sql, stmt)
                self.cur.execute(sql, stmt)
            self.con.commit()
            return 1
        except Exception as e:
            print(e)
            return 0

    def toJSON(self, data):
        try:
            dt = {"data": []}
            for x in data:
                dt["data"].append(x)
            print(dt)
            return dt
            exit()
        except Exception as e:
            print(e)
            # print("Error ToJSON: "+e)
            exit()
            # return "tidak"
