

+ Looking at the files given we can see that the flag.txt is in php.caddy.chal-kalmarc.tf directory but as php is disabled(this can be seen from the Caddyfile - commented php_fastcgi) we cant simple traverse to the file and access that. 
+ From the docker file we can see the following line:
`cp -r *.caddy.chal-kalmarc.tf backups/ && rm php.caddy.chal-kalmarc.tf/flag.txt && sleep 1 && caddy run"`
+ It is clear from the above line that all the files from the webserver is copied to /backup directory and flag.txt file is removed from the php vhost. So, as it was copied to /backup, the flag file will still be in that directory. 
+ So, we can give the host as: backups/php.caddy.chal-kalmar.tf.
+ Now it will allow to access the served files from different folders/vhosts.
+ Also, if we try to get /flag.txt, it will give forbidden error, to bypass this use /../flag.txt.
+ Flag: `kalmar{th1s-w4s-2x0d4ys-wh3n-C4ddy==2.4}`
+ If you do ../ on the root you still reference the same directory. Much like on linux if you are on the / (root) -> doing cd ../ will not do anything, since it is the same path -> just specifying the root path like this will be just different enoughto bypass the path in 403 caddy directive.
