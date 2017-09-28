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

