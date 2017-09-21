import sys
from db import Db

class Uids:

    def addUid(self, uid):
        d = Db()
        connection = d.getConnection()
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `uid` FROM `uids` WHERE `uid`=%s"
                cursor.execute(sql, (uid,))
                result = cursor.fetchone()
                if result:
                    print(result)
                else:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO `uids` (`uid`) VALUES (%s)"
                        cursor.execute(sql, (uid))

                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        connection.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
 