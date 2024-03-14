# 1. PONG:

## Challenge description:
Some random websites can ping hosts.

## Solution:
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
My intern configured my iOS app and my website to handle deeplinks, but they didnt tell me the path. :( Can you help me find it??<br>

## Solution:
So, when we open the page, it says `nothing is here`. So, the challenge description says something about paths.So we use `dirsearch` command. This command is used and designed to brute force directories and files in webservers, AKA web path scanner. <br>
So, in terminal,<br>
`dirsearch -u 01.linux.challenges.ctf.thefewchosen.com:54245`<br>
After executing the above command, we get a file path as: `/.well-known/apple-app-site-association`.<br>
So, when we visit the above directory,<br>
`01.linux.challenges.ctf.thefewchosen.com:54245/.well-known/apple-app-site-association`, we get a file to be downloaded.<br>
When we open the apple-app-site-association file we get the flag there in the path field.<br>
Flag: TFCCTF{4appl3_4pp_5lt3_4550c14t10n}<br>

# 3. CALENDER

## Challenge Description:
Are online calenders trust worthy??
Flag format: TFCCTF{foundpassword}

# Solution:
+ Word press challenge<br>
+ reference: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/wordpress<br>
+ When we get a wordpress challenge, first we need to look for default directories.<br>
+ So, we tried looking for `/wp-includes`, `/wp-contents`,`wp-json/wp/v2/users/`. All these dircetories were forbidden.<br>
+ lets look at `/wp-admin/`, this is where we login for the wordpress site.<br>
+ When we try entering the username and password, it says password incorrect. So, as we know the purpose of the challenge is to find the password.<br>
+ So, while looking at the source code of the challenge we can see a `/wp-scan/plugins/` named modern-events-calender-lite.<br>
+ So, when we search for the exploit for `modern-events-calender-lite`, we get the following reference:<br>
https://www.exploit-db.com/exploits/50084<br>
+ So, we can see an exploit url as `http://' + target_ip + ':' + target_port + wp_path + '/wp-admin/admin.php?page=MEC-ix&tab=MEC-export&mec-ix-action=export-events&format=csv`<br>
+ So, for this challenge,<br>
`01.linux.challenges.ctf.thefewchosen.com:54423/wp-admin/admin.php?page=MEC-ix&tab=MEC-export&mec-ix-action=export-events&format=csv` this url gives the password for the admin username which is what we want.<br>
Flag: TFCCTF{WPNe3MgF$sNj8E8F6d}


# 4. DIAMONDS







