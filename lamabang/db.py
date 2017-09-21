import pymysql.cursors

class Db:
    def getConnection(self):
        connection = pymysql.connect(host='localhost',
                        user='root',
                        password='',
                        db='test',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
        return connection