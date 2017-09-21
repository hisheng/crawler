import pymysql.cursors

connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `uid` FROM `uids` WHERE `uid`=%s"
        cursor.execute(sql, ('hisheng',))
        result = cursor.fetchone()
        if result:
            print(result)
        else:
            print('haha')


    with connection.cursor() as cursor:
        sql = "INSERT INTO `uids` (`uid`) VALUES (%s)"
        cursor.execute(sql, ('webmaster@python.org'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
finally:
    connection.close()