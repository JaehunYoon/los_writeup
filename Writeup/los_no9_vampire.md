# Lord of SQL Injection No.9 Vampire

Vampire 문제는 `str_replace`의 취약점을 찾아 우회하여 원하는 `id`값을 삽입할 수 있도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/\'/i', $_GET[id])) exit("No Hack ~_~"); 
  $_GET[id] = str_replace("admin","",$_GET[id]); 
  $query = "select id from prob_vampire where id='{$_GET[id]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id'] == 'admin') solve("vampire"); 
  highlight_file(__FILE__); 
?>
```

```php
$_GET[id] = str_replace("admin","",$_GET[id]);
```

`$_GET[id]` 방식으로 받은 `id`값을 `str_replace` 함수를 통해 `admin` 이라는 문자열을 빈 문자열로 바꾼다.

#### str_replace

`str_replace` 함수는 가장 마지막에서 받은 값에서 첫 번째에 주어진 문자열을 두 번째 문자열로 치환하는 함수이다.

* [php.net - str_replace](http://php.net/manual/kr/function.str-replace.php)

* [php str_replace의 사용법](https://blog.simpleuser.net/93/php-str_replace%EC%9D%98-%EC%82%AC%EC%9A%A9%EB%B2%95/)

#### 문제 풀이 조건

```php
if($result['id'] == 'admin') solve("vampire");
```

`$_GET` 방식으로 입력받은 `id`값이 `admin`과 일치하면 문제 풀이에 성공한다.

## Solution

```
http://los.eagle-jump.org/vampire_***.php?id=Admin
```

`str_replace` 함수도 `admin` 중 최소한 한 글자만 대문자로 바꿔주면 `admin`과 같은 문자열이라고 인식하지 못하고 sql에서 대소문자를 구분하지 않는 원리를 이용하여 문제 풀이에 성공하게 된다.

```
http://los.eagle-jump.org/vampire_***.php?id=adadminmin
```

`str_replace` 함수는 1회만 수행하기 때문에 `admin` 이라는 문자열 사이에 `admin` 문자열을 끼워 넣어 `str_replace`로 문자열을 1회만 공백으로 치환한 후, `id`값에 `admin`만 남게 하면 문제 풀이에 성공하게 된다.