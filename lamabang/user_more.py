import sys,requests,pymysql.cursors




connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)



if len(sys.argv ) > 1 :
    url = sys.argv[1:]
else:
    url = 'http://www.lamabang.com/user-more/u-6A73765E68736E16694D7E1A-tab-3.html'

bodyString = requests.get(url)


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
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `uid` FROM `uids` WHERE `uid`=%s"
            cursor.execute(sql, (uid,))
            result = cursor.fetchone()
            if result :
                print(result)
            else:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `uids` (`uid`) VALUES (%s)"
                    cursor.execute(sql, (uid))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()
    except :
        print("Unexpected error:", sys.exc_info()[0])



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

index = 0
s = bodyString.text[index:]

while True :
    url,index = getUrl(s)
    if url :
        s = s[index:]
    else:
        break
    print (url,index)
    if isUserMore(url) > 0:
        print (url, index)


