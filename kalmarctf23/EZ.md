Since PHP is disabled (this can be seen from the Caddyfile - commented php_fastcgi) this means that traversing to the https://php.caddy.chal-kalmarc.tf/index.php will not call the PHP interpreter to evaluate the code and instead just echo the code out.  Caddy webserver looks at the Host header value and depending on it allows access to the served files from different folders/vhosts. From the docker setup file it is apparent that all web server's contents are copied to backups/ folder and flag.txt is removed from the php.caddy.chal-kalmarc.tf vhost. With the Host value set to the 'backups/' all files from the 'backups' folder become accessible, including the php.caddy.chal-kalmarc.tf folder in which is a flag. The last obstacle is to bypass respond /flag.txt 403 directive. By prepending /../ in the URL we can bypass this restriction and access the flag.txt without 403 forbidden.

+ Looking at the files given we can see that the flag.txt is in php.caddy.chal-kalmarc.tf directory but as php is disabled(this can be seen from the Caddyfile - commented php_fastcgi) we cant simple traverse to the file and access that. 
+ From the docker file we can see the following line:
`cp -r *.caddy.chal-kalmarc.tf backups/ && rm php.caddy.chal-kalmarc.tf/flag.txt && sleep 1 && caddy run"`
+ It is clear from the above line that all the files from the webserver is copied to /backup directory and flag.txt file is removed from the php vhost. So, as it was copied to /backup, the flag file will still be in that directory. 
+ So, we can give the host as: backups/php.caddy.chal-kalmar.tf.
+ Now it will allow to access the served files from different folders/vhosts.
+ Also, if we try to get /flag.txt, it will give forbidden error, to bypass this use /../flag.txt.
+ Flag: `kalmar{th1s-w4s-2x0d4ys-wh3n-C4ddy==2.4}`
