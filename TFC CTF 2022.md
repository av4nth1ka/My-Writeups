# 1. PONG:

## Challenge description:
Some random websites can ping hosts.

# Solution:
So, the page says `command executed: ping -c 127.0.0.1` <br>
So, the url looks like:<br>
`01.linux.challenges.ctf.thefewchosen.com:54133/index.php?host=127.0.0.1`<br>
So, whatever we give the place of host will be changed in the page as well.<br>
So, lets see what the following url gives:<br>
`01.linux.challenges.ctf.thefewchosen.com:54133/index.php?host=127.0.0.1; ls`<br>
It gives the output as : index.php<br>
In bash we know that if we use a semicolon(;) we know that it will connect different statements. So, the ls command got executed here and gave the output as index.php.<br>
So, lets try `ls` ing the root directory. There we can see multiple files and one among the file is `flag.txt`. So lets see what we by `cat` ing flag.txt.<br>
`01.linux.challenges.ctf.thefewchosen.com:54133/index.php?host=127.0.0.1; cat flag.txt`<br>
Here we get the flag!!!<br>
Flag: TFCCTF{c0mm4nd_1nj3c51on_1s_E4sy}


# 2. DEEPLINKS

## Challenge Desciption:
My intern configured my iOS app and my website to handle deeplinks, but they didnt tell me the path. :( Can you help me find it??

## Solution:


