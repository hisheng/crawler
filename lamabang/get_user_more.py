import sys,requests,time
from db import Db
max = 1
guid = '69636E15695D76136A401A1A'
def getuidNoMore():
    d = Db();
    connect = d.getConnection()
    try:
        with connect.cursor() as cursor:
            sql = "SELECT * FROM `uids` where more = 0 limit 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
    except:
        return 0

def getUrl(body):
    a = body.find('href=')
    if a == -1:
        return None, 0
        # print (a)
    first = body[a:].find('"')
    # print (first)
    second = body[a + first + 1:].find('"')
    # print (second)
    url = body[a + first + 1: a + second + first + 1]
    return url, a + second + first + 1


def addUserMore(uid ,max):
    d = Db()
    connect = d.getConnection()
    try:

        if not getUserMore(uid):
            with connect.cursor() as cursor:
                sql = "INSERT INTO `user_more` (`uid`,`page_num`) VALUES (%s,%s)"
                cursor.execute(sql, (uid, max))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connect.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])

# 检查是否是 user_more
def isUserMorePage(url):
    u = url.find('u-')
    page = url.find('page')
    if(u > 0 and page > 0):
        uid_ = url[u+2:page-6]
        end = uid_.find('-')
        global max
        global guid
        num = url[page + 5:]
        if int(num) > int(max) :
            max = num
        if guid != uid_[:end] :
            addUserMore(guid ,max)
            guid = uid_[:end]
            max = 1
        return 1
    else:
        return -1

# 爬虫 爬某个url
def crawlerUrl(url):
    bodyString = requests.get(url)
    index = 0
    s = bodyString.text[index:]
    while True:
        url, index = getUrl(s)
        if url:
            s = s[index:]
        else:
            break
        #print(url, index)
        if isUserMorePage(url) > 0:
            print(url, index)





def setUserMore(uid):
    url = "http://www.lamabang.com/user-more/u-" + uid + "-tab-3.html"
    print(url)
    crawlerUrl(url)




def getUserMore(uid):
    d = Db()
    connect = d.getConnection()
    try:
        with connect.cursor() as cursor:
            sql = "SELECT * FROM `user_more` where uid = %s limit 1"
            cursor.execute(sql,uid)
            result = cursor.fetchone()
            # print(result)
            return result
    except:
        return 0

def setUidsMore(uid):
    d = Db()
    connect = d.getConnection()
    try:
        with connect.cursor() as cursor:
            sql = "UPDATE `uids`  SET `more`  = 1 WHERE  `uid` = %s"
            cursor.execute(sql, (uid))
            connect.commit()
    except:
        return 0

print('start')


while getuidNoMore():
    user = getuidNoMore()
    # print(user)
    if not user :
        break

    uid = user['uid']
    # print(uid)
    usermore = getUserMore(uid)
    if not usermore :
        setUserMore(uid)
    setUidsMore(uid)
    time.sleep(6)


