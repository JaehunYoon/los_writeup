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