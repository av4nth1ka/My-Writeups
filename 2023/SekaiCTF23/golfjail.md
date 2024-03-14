+ you have a website where you need to trigger an XSS and then you must send the malicious link to the administrator (a bot program) which will visit the provided URL and will get the XSS triggered.
```
<?php
    header("Content-Security-Policy: default-src 'none'; frame-ancestors 'none'; script-src 'unsafe-inline' 'unsafe-eval';");
    header("Cross-Origin-Opener-Policy: same-origin");

    $payload = "🚩🚩🚩";
    if (isset($_GET["xss"]) && is_string($_GET["xss"]) && strlen($_GET["xss"]) <= 30) {
        $payload = $_GET["xss"];
    }

    $flag = "SEKAI{test_flag}";
    if (isset($_COOKIE["flag"]) && is_string($_COOKIE["flag"])) {
        $flag = $_COOKIE["flag"];
    }
?>
<!DOCTYPE html>
<html>
    <body>
        <iframe
            sandbox="allow-scripts"
            srcdoc="<!-- <?php echo htmlspecialchars($flag) ?> --><div><?php echo htmlspecialchars($payload); ?></div>"
        ></iframe>
    </body>
</html>
```
+ we can execute JavaScript code and eval because of unsafe-inline and unsafe-eval but as the default-src is set to none, admin wont be able to visit the our controlled website to get the cookie(flag)
+ we have a parameter called xss which is filtered with `htmlspecialchars` and is included within the srcdoc of a iframe tag.
+ value in the parameter xss should a string and the length of the string should be less than 30 chars
+ the iframe used here is sandboxed, only scripts is allowed. The iframe we control inherits the csp policy of its parent
![image](https://github.com/av4nth1ka/My-Writeups/assets/80388135/7ba54f1f-40c7-488c-b153-d08672d6415a)

So basically we have 2 main problems:

1. Find a way to execute arbitrary XSS using only <= 30 characters (!)
2. Bypass the CSP policy to let the admin execute our payload and exfiltrate the cookie flag

+ We can execute xss by including eval but the character limit is 30 only
+ we can use a uri fragment identifier
`https://www.example.com?param1=x&param2=y#This_is_the_fragment_identifier`
+ In JavaScript we can access this value by using the location.hash property
+ https://golfjail.chals.sekai.team/golfjail.php?xss=<svg/onload=eval(location.hash)>
but this is 32 characters long. even if we execute this payload location.hash would return the empty string ''. That’s because the iframe location object is sandboxed from the parent window
+ Any Node of the DOM, has a property named baseURI. This property returns absolute base URL of the document containing the node.
+ So this property allows us to retrieve the entire URI (which include the URI fragment where we can place our arbitrary XSS to execute)
Payload:` https://golfjail.chals.sekai.team/?xss=%3Csvg/onload=eval(%22%27%22%2bbaseURI)%3E#';console.log(1)`
Which is a valid JavaScript expression and has the effect of printing 1 to the console. We have now arbitrary XSS payload execution



