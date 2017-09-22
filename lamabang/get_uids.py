import sys,requests,pymysql.cursors
from db import Db
from uids import Uids
import time



connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)






def getUid(url):
    u = url.find('u-')
    html = url.find('.html')
    uid = url[u+2:html]
    print(uid)
    if u > 0 and html > 0 :
        end = uid.find('-')
        if end > 0:
            uid = uid[:end]
        addUid(uid)



def getUrl(body):
    a = body.find('href=')
    if a == -1 :
        return None,0
   # print (a)
    first = body[a :].find('"')
    #print (first)
    second = body[a+first+1 :].find('"')
    #print (second)
    url = body[a + first + 1: a +second+first+1]
    getUid(url)
    return  url,a +second+first+1

max = 1
uid = '6A73765E68736E16694D7E1A'

def addUserMore(uid ,max):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `user_more` (`uid`,`page_num`) VALUES (%s,%s)"
            cursor.execute(sql, (uid, max))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])


def addUid(uid):
     u = Uids()
     u.addUid(uid)



# 检查是否是 user_more
def isUserMore(url):
    u = url.find('u-')
    page = url.find('page')
    if(u > 0 and page > 0):
        uid_ = url[u+2:page-6]
        end = uid_.find('-')
        global uid
        global max
        num = url[page + 5:]
        if int(num) > int(max) :
            max = num
        if uid != uid_[:end] :
            addUserMore(uid ,max)
            uid = uid_[:end]
            max = 1

        print (uid)

        return 1
    else:
        return -1

# 取得 user_more page最大值
def maxUserMorePage(url):
    return 1



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
        print(url, index)
        if isUserMore(url) > 0:
            print(url, index)


if len(sys.argv ) > 1 :
    url = sys.argv[1:]
else:
    url = 'http://www.lamabang.com/user-more/u-6A73765E68736E16694D7E1A-tab-3.html'


def getUserMore():
    db = Db()
    dbconnection = db.getConnection()
    try:
        with dbconnection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `*` FROM `user_more` where  `status` = 1 limit 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
    except:
        return 0

def offUserMore(id):
    db = Db()
    dbconnection = db.getConnection()
    try:
        with dbconnection.cursor() as cursor:
            # Read a single record
            sql = "UPDATE `user_more`  SET `status`  = %s WHERE  `id` = %s"
            cursor.execute(sql, ('0',id))
            connection.commit()
    except:
        return 0

def setUserMoreStart(id,start):
    db = Db()
    dbconnection = db.getConnection()
    try:
        with dbconnection.cursor() as cursor:
            # Read a single record
            sql = "UPDATE `user_more`  SET `start`  = %s WHERE  `id` = %s"
            cursor.execute(sql, (start, id))
            connection.commit()
    except:
        return 0

def getLamabangUserMoreUrl(uid):
    url = "http://www.lamabang.com/user-more/u-"+ uid +"-tab-3.html?page="
    return  url

while getUserMore() :
    r = getUserMore()
    id = r['id']
    uid = r['uid']
    num = r['page_num']
    i = r['start']
    while i <= num:
        page = getLamabangUserMoreUrl(uid) + str(i)
        print(page)
        time.sleep(6)
        crawlerUrl(page)
        setUserMoreStart(id,i)
        i = i+1
    offUserMore(id)





