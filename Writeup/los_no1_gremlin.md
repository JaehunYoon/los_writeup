# Lord of SQL Injection No.1 - Gremlin

LOS Gremlin 문제는 기본적인 SQL Injection 문법으로 SQL문을 우회하도록 유도한 문제이다.

## 소스 코드

gremlin 단계에서 문제를 해결해야 할 php 소스코드는 다음과 같다.
```php
<?php
  include "./config.php";
  login_chk();
  dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); // do not try to attack another table, database!
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysql_fetch_array(mysql_query($query));
  if($result['id']) solve("gremlin");
  highlight_file(__FILE__);
?>
```
## include
```php
  include "./config.php";
  login_chk();
  dbconnect();
  ...
  if($result['id']) solve("gremlin");
  ...
```
PHP 코드 중 include 부문의 라인이다.
include는 PHP에서 다른 PHP 파일을 코드 안으로 불러와서 사용할 때에 사용된다.
위의 login_chk(), dbconnect(), solve() 함수는 공개된 PHP 코드 내에서 함수의 정의 부분이 보이지 않기 때문에, include를 통해 config.php 라는 외부 PHP 파일에서 호출된다는 것을 알 수 있다.

#### include 알아보기

* [생활코딩 - PHP / include와 namespace](https://opentutorials.org/course/62/5138)

* [php.net - include](http://php.net/manual/kr/function.include.php)

## preg_match
```php
  ...
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); // do not try to attack another table, database!
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  ...
```
코드를 살펴보면 preg_match 함수를 통해 GET 방식으로 입력받은 id와 pw 문자열을 비교하게 되는데, 이 때 입력받은 문자열에 `prob`, `_`, `.`, `\`, `()` 가 하나라도 포함되면 `No hack ~_~` 이라고 화면에 출력하면서 문제 풀이를 실패했다는 것을 알린다.

* `preg_match`는 PHP에서 정규표현식 매치를 수행한다.
* `preg_match`에서 최대 매치 횟수는 1번이기 때문에 첫번째 매치가 이루어지면 실행을 중지한다.
* 매치가 된 횟수는 최대 1이기 때문에, 실행을 중지 한 후에는 매치 횟수 0 또는 1을 반환한다.
* 오류가 발생하면 FALSE를 반환한다.

### No Hack 출력 예시
```
http://los.eagle-jump.org/gremlin_***.php?id=\ …
```
이런 식으로 id나 pw에 preg_match에서 매치를 시키는 정규표현식이 들어가게 한 후 Enter를 누르면 `No Hack ~_~`의 결과가 출력된다.

#### preg_match 알아보기
* [php.net - preg_match](http://php.net/manual/kr/function.preg-match.php)

* [Opentutorials.org - 문자열 연산과 정규 표현식(2)](https://opentutorials.org/course/779/4935)

#### 정규표현식 알아보기
* [Opentutorials.org - 정규 표현식 패턴들](https://opentutorials.org/module/622/5143)
* [생활코딩 - 정규 표현식](https://opentutorials.org/course/62/5141)
* [표현식](http://ult-tex.net/info/perl/)
* [위키백과 - 정규 표현식](https://ko.wikipedia.org/wiki/%EC%A0%95%EA%B7%9C_%ED%91%9C%ED%98%84%EC%8B%9D)
* [nextree - 정규 표현식을 소개합니다](http://www.nextree.co.kr/p4327/)

#### $GET[] 알아보기
* GET 방식은 데이터를 전송할 때 URL에 데이터를 포함시켜 전달하는 것이다.
* POST 방식은 GET과는 다르게 데이터를 URL에 포함시키지 않고 전송할 수 있다.
* [생활코딩 - 입출력 그리고 폼과 HTTP](https://opentutorials.org/course/62/5125)

```php
<?php
  …
  $query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysql_fetch_array(mysql_query($query));
  …
?>
```
위의 코드를 보면 `$_GET` 방식으로 받은 id와 pw가 `$_query`에 직접 삽입되는 것을 알 수 있다. 

* `mysql_auery($query)` : query에 넣어둔 값을 $result 변수에 저장한다.
* `mysql_fetch_array()` : 연관 색인 및 숫자 색인으로 된 배열로 결과 행을 반환한다.

#### 문제 해결 조건
```php
  if($result['id']) solve("gremlin");
  highlight_file(__FILE__);
?>
```
코드의 if문을 해석해보면, id값이 존재하면 `solve`, `highlight_file` 함수가 실행되고 문제 풀이를 성공하게 된다.

즉, 그냥 쿼리문을 실행하기만 하면 문제를 풀 수 있는 것이다.

## Solution

```
  http://los.eagle-jump.org/gremlin_***.php?id=' or 1=1 -- ;
```
`&_GET`으로 정보를 전송하기 위해서 URL 뒤에 쿼리스트링을 추가한다.
id에 '를 넣어 id 입력을 마치고 `or 1=1 --`라는 기본적인 SQL injection 문법을 이용하여 문제 풀이를 성공할 수 있다.

```sql
  select id from prob_gremlin where id='' or 1=1 -- ;'
```
* `or 1=1` 은 SQL 문의 WHERE 절을 무력화시키는 기본적인 삽입 문법인데, `or 1=1` 이라는 것이 WHERE절을 항상 참으로 만들어 `prob_gremlin`의 모든 id를 불러온다.

* `or 1=1` 뒤의 `--`는 뒤에 오는 모든 내용들을 무력화시키는 주석문이기 때문에 pw를 입력하지 않아도 된다.

* `-- ; `에서 주석 처리 부분만 입력하면 정상적으로 주석 처리가 되지 않기 때문에 `--` 뒤에 공백 후 `;`를 추가했다. 그리고, `--` 뒤에 공백이나 #만 추가하면 처리과정에서 생략이 되기 때문에 %20을 직접 입력하거나 공백 후 아무 문자를 삽입해야한다.