import sys,requests

if len(sys.argv ) > 1 :
    url = sys.argv[1:]
else:
    url = 'http://www.lamabang.com/user-more/u-6A73765E68736E16694D7E1A-tab-1.html'

bodyString = requests.get(url)




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
    return  url,a +second+first+1




index = 0
s = bodyString.text[index:]

while True :
    url,index = getUrl(s)
    if url :
        s = s[index:]
    else:
        break
    print (url,index)


