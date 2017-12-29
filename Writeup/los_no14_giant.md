# Lord of SQL Injection No.14 Giant

Giant 문제는 `공백(Whitespace)`, `\n`, `\r`, `\t` 를 사용하지 않고 공백 효과를 내는 방법을 알아보는 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(strlen($_GET[shit])>1) exit("No Hack ~_~"); 
  if(preg_match('/ |\n|\r|\t/i', $_GET[shit])) exit("HeHe"); 
  $query = "select 1234 from{$_GET[shit]}prob_giant where 1"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result[1234]) solve("giant"); 
  highlight_file(__FILE__); 
?>
```

```php
$query = "select 1234 from{$_GET[shit]}prob_giant where 1"; 
```
`$_GET` 방식으로 `shit`을 query에 직접 대입한다.

```php
if(strlen($_GET[shit])>1) exit("No Hack ~_~");
```

입력받은 `shit`의 문자열의 길이가 1보다 크면 `No Hack  ~_~`을 출력하고 문제 풀이에 실패하게 된다.

`strlen` 함수는 문자열의 길이를 체크하여 그 길이만큼 반환하는 함수이다.

#### strlen

* [php.net](http://php.net/manual/kr/function.strlen.php)

```php
if(preg_match('/ |\n|\r|\t/i', $_GET[shit])) exit("HeHe");
```

`preg_match` 에서 `공백(Whitespace)`, `\n`, `\r`, `\t`을 필터링을 하면 `HeHe`를 출력하고 문제 풀이에 실패하게 된다.

#### 문제 풀이 조건

```php
if($result[1234]) solve("giant");
```

`select 1234 ...` 와 같은 sql문에서 결과값이 존재하면 문제 풀이에 성공하게 된다.
즉, `$_GET[shit]`의 문자열이 1 이하이며 `preg_match`에 필터링 되는 문자를 사용하지 않고 입력하면 문제 풀이에 성공할 수 있다.

## Solution

공백 효과를 내는 문자들이 일부 필터링이 되어있는 것을 확인했을 것이다.
하지만 이번에도 `No.5 Wolfman` 문제에서 찾아보았던 공백 우회 문자들을 다시 참고해볼 수 있다.

* [공백을 우회하는 No.5 Wolfman writeup 다시보기](https://github.com/JaehunYoon/los_writeup/blob/master/los_no5_wolfman.md)

* Tap (%09) // URL에서 사용된 대체 문자.
* Line Feed (%0A)
* Vertical Tab (%0B)
* Form Feed (%0C)
* Carriage Return (%0D)

이 공백 우회 문자들 중에서 현재 필터링된 문자들을 제외해보면,

* Vertical Tab (%0B)
* Form Feed (%0C)

위의 두 문자를 이용할 수 있다.

```
http://los.eagle-jump.org/giant_***.php?shit=%0B
```

위와 같이 `Vertical Tab`을 사용하거나,

```
http://los.eagle-jump.org/giant_***.php?shit=%0C
```

`Form Feed`를 사용하면 문제 풀이 조건을 충족하여 문제 풀이에 성공하게 된다.