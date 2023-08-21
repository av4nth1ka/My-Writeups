Given the code:
```
<?php
            define("LOADFLAG", true);
            error_reporting(0);
            function get_debug_info($filters) {
                ob_start(); phpinfo(); $pi = ob_get_contents(); ob_end_clean() ;
                $debug = array();
                foreach(explode(PHP_EOL, $pi) as $line) {
                    if(strstr($line, $filters)) {
                        array_push($debug, $line);
                    }
                }
                return $debug;
            }
            if(isset($_GET['action']) && $_GET['action']=="debug") {
                $is_admin = $_SERVER['REMOTE_ADDR'] == "127.0.0.0" ? 1 : 0;
                $debug_info = get_debug_info(extract($_GET['filters']));
                if($is_admin) {
                    echo implode($debug_info, '\n');
                } else {
                    echo("Only local admins are allowed to debug!");
                }
                include_once "flag.php";
            }
            if(isset($_GET['action']) && $_GET['action']=="src") {
                highlight_file(__FILE__);
            }
            // With <3 from @gehaxelt.
        ?>
```
+ `$is_admin = $_SERVER['REMOTE_ADDR'] == "127.0.0.0" ? 1 : 0;`
  This line of code checks whether the remote IP address of the user making the request ($_SERVER['REMOTE_ADDR']) is equal to the IP address "127.0.0.0". If the condition is true, it sets the value of the variable $is_admin to 1; otherwise, it sets the value to 0.

+ While solving the challenge, we spend more time in trying the ip-spoofing using the headers like X-forwarded for, X-Client-IP and X-Real IP. But we were in the wrong path. Should have checked what each function does :(
+ Lets come to the manual of extract() in php
  https://www.php.net/manual/en/function.extract.php
  ![image](https://github.com/Avanthikaanand/My-Writeups/assets/80388135/d03cdcc1-4fe3-4463-acff-99ca1217c40f)
  ![image](https://github.com/Avanthikaanand/My-Writeups/assets/80388135/b09fae30-6b0d-4dee-872f-ad4f297a00bf)
+ extract() can overwrite local variables, so u just change the value of is_admin to 1
+ So, we can just give `?action=debug&filters[is_admin]=1`.
  




