# Lord of SQL Injection No.8 Troll

Troll 문제는 `admin`을 필터링하는 `ereg` 함수의 취약점을 찾아 우회하여 원하는 `id`값을 삽입하도록 유도한 문제이다.

## 소스 코드
```php
<?php  
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/\'/i', $_GET[id])) exit("No Hack ~_~");
  if(@ereg("admin",$_GET[id])) exit("HeHe");
  $query = "select id from prob_troll where id='{$_GET[id]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysql_fetch_array(mysql_query($query));
  if($result['id'] == 'admin') solve("troll");
  highlight_file(__FILE__);
?>
```

```php
if(@ereg("admin",$_GET[id])) exit("HeHe");
```

`ereg`는 문자열을 체크하는 함수이다.
`preg_match`와는 달리 문자열을 필터링하는 함수로 `admin`을 만나면 `HeHe`를 출력하며 문제 풀이에 실패하게 된다.

#### ereg

* [php.net - ereg](http://php.net/manual/kr/function.ereg.php)

`ereg` 앞에 붙은 `@`는 php에서 오류가 발생하더라도 오류 메시지를 표시하지 않겠다는 의미이다.


#### 문제 풀이 조건

```php
if($result['id'] == 'admin') solve("troll");
```

입력받은 `id` 값이 문자열 `admin`과 일치하면 문제 풀이에 성공하게 된다.

## Solution

```
http://los.eagle-jump.org/troll_***.php?id=Admin
```

`ereg` 함수의 취약점에는 `NULL` 문자를 만나면 문자열 체크를 더 이상 진행하지 않게 되는 문제가 있고, 대소문자 필터링이 불가능하다는 점이 있다.

이 문제를 해결하는 데에는 '대소문자 필터링 불가' 라는 `ereg` 함수의 취약점을 이용하여 `id`값에 `admin` 중 최소한 한 글자 이상 소문자를 대문자로 바꾸어주면 `sql`에서 대소문자 구분을 하지 않아 `admin`과 같은 문자열로 인식을 하여 문제 풀이 조건에 충족하면서 문제 풀이에 성공하게 된다.