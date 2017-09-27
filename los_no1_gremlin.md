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