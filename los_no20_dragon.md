# Lord of SQL Injection No.20 Dragon

Dragon 문제는 주석처리로 무력화된 절을 우회하여 사용할 수 있도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_dragon where id='guest'# and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("dragon");
  highlight_file(__FILE__); 
?>
```

```php
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
```

`preg_match` 함수에서 필터링 하는 문자들이다. `&_GET` 방식으로 입력받은 `pw`값에 위의 문자들이 포함되면 `No Hack ~_~` 을 출력시키며 문제 풀이에 실패하게 된다.

```php
$query = "select id from prob_dragon where id='guest'# and pw='{$_GET[pw]}'";
```

query문을 살펴보면 `id='guest'` 와 `and pw=` 사이에 `#`이 포함되어 있다.

이는 `pw`를 `$_GET` 방식으로 입력받기 때문에 가능했던 SQL 삽입 공격 절을 포함하여 `#` 뒤에 오는 모든 절을 무력화시킨다.

#### 문제 풀이 조건

```php
 if($result['id'] == 'admin') solve("dragon");
```

`id` 값이 `admin`과 일치하면 문제 풀이에 성공하게 된다.

## Solution

SQL 삽입 공격 절을 무력화시키는 주석을 우회하고 원하는 SQL문을 삽입하면 문제를 풀 수 있다.

SQL문의 주석은 **한 라인**에서 `#` 뒤에 오는 모든 절을 무력화시킨다.

한 라인에서만 유효한 주석이기 때문에 이를 이용하면 되는데, `$_GET` 방식으로 입력받는 `pw`에 개행문자 (\n)을 포함시키면 SQL문 자체에서 개행 처리가 되어 다음 줄에서 계속하여 SQL문이 실행된다.
즉, 개행을 사용하면 `#`가 아무리 뒤에 오는 절을 무력화시키더라도 다음 줄에서 원하는 SQL문을 수행하면 된다.

```
http://los.eagle-jump.org/dragon_7ead3fe768221c5d34bc42d518130972.php?pw=%27%0A%20and%20pw=%27123%27%20or%20id=%27admin%27%20--%20;
```

`pw='\n and pw='123' or id='admin' -- ;` 를 삽입하여 개행을 시켜준 후 조건에 맞게 `id`값을 `admin`으로 만들어주면 문제 풀이에 성공하게 된다.