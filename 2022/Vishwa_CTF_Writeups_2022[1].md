Writeups

1. My Useless Website:

Description - I made this website with simple authentication used in it. But unfortunately I forgot the credentials. Can you help me to find the correct one ??

` `Url -[ ](https://my-us3l355-w3b51t3.vishwactf.com/)<https://my-us3l355-w3b51t3.vishwactf.com/>

Solution: SQL injection possible

Given the title as Admin login. So maybe the username will be “admin”

So, in username, giving admin’-- gives the flag.

Flag: **VishwaCTF{I\_Kn0w\_Y0u\_kn0W\_t1hs\_4lr3ady**}


1. Hey Buddy:

Hey Buddy, Give me your name. I will display your name on my website. Yes exactly, there is nothing on this website.

Url - <https://h3y-buddy.vishwactf.com/>

1. Stock Bot:

Description: We have our online shop of computer related accessories. So for easy customer interaction we have made a stock bot which will give you how many units of enlisted products are available. <https://st0ck-b0t.vishwactf.com/>

Solution: 

Given a hint in the view page source that “Along with other products the Flag is also available in the Products direcAlong with other products the Flag is also available in the Products directory”


|function sendMsg() {||
| :- | :- |
||var msg = document.querySelector('#input-msg').value;|
||document.querySelector('#input-msg').value = "";|
||div = document.querySelector('.chat-body');|
||div.innerHTML += "<div id='user-chat' class='user-div'><p class='user-msg msg'>" + msg + "</p></div>";|
||div.scrollTop = div.scrollHeight;|
||if(!msg.includes('Flag')){|
||async function fetchDataAsync(url) {|
||try {|
||const response = await fetch(url);|
||obj = (await response.json());|
||div.innerHTML += "<div class='bot-div'><img src='bot.png' class='bot-avatar' /><p class='bot-msg msg'>"+obj['Quantity']+"</p></div>"|
||} catch (error) {|
||div.innerHTML += "<div class='bot-div'><img src='bot.png' class='bot-avatar' /><p class='bot-msg msg'>No such product</p></div>"|
||}|
||div.scrollTop = div.scrollHeight;|
||}|
||fetchDataAsync('/Products/check.php?product='+msg);|
||}|
||else{|
||div.innerHTML += "<div class='bot-div'><img src='bot.png' class='bot-avatar' /><p class='bot-msg msg'>No such product</p></div>"|
||div.scrollTop = div.scrollHeight;|
||}|
||}|

So, from the above code we can understand that the flag is been fetched from “/Products/check.php?product=”

So we gave “<https://st0ck-b0t.vishwactf.com/Products/check.php?product=Flag>”

And we got the flag.

Flag: **VishwaCTF{b0T\_kn0w5\_7h3\_s3cr3t}**

1. **To-do list:**

Simple Todo list website to manage your tasks. Use it wisely. <https://t0-d0-l1st.vishwactf.com/>

Solution: 





1. Flag-collection:

Link: <https://iosiro.com/blog/baserunner-exploiting-firebase-datastores>

link:<https://book.hacktricks.xyz/pentesting/pentesting-web/buckets/firebase-database>

<https://github.com/APWB/VishwaCTF-2022-writeups>


Strong Encryption:

<?php

`    `// Decrypt -> 576e78697e65445c4a7c8033766770357c3960377460357360703a6f6982452f12f4712f4c769a75b33cb995fa169056168939a8b0b28eafe0d724f18dc4a7

`    `$flag="";

`    `function encrypt($str,$enKey){

`        `$strHex='';

`        `$Key='';

`        `$rKey=69;

`        `$tmpKey='';

`        `for($i=0;$i<strlen($enKey);$i++){

`            `$Key.=ord($enKey[$i])+$rKey;

`            `$tmpKey.=chr(ord($enKey[$i])+$rKey);

`        `}   

`        `echo "Key:".$Key."\n";



`        `$rKeyHex=dechex($rKey);

`        `echo "rKeyHex:".$rKeyHex."\n";

`        `$enKeyHash = hash('sha256',$tmpKey);

`        `echo "enKeyHash:".$enKeyHash."\n";

`        `for ($i=0,$j=0; $i < strlen($str); $i++,$j++){

`            `if($j==strlen($Key)){

`                `$j=0;

`            `}

`            `$strHex .= dechex(ord($str[$i])+$Key[$j]);



`        `}

`        `echo "strHex:".$strHex."\n";

`        `$encTxt = $strHex.$rKeyHex.$enKeyHash;

`        `return $encTxt;

`    `}

`    `$encTxt = encrypt($flag, "VishwaCTF");

`    `echo "encTxt:".$encTxt."\n";

?>

Output:

Key:155174184173188166136153139

rKeyHex:45

enKeyHash:2f12f4712f4c769a75b33cb995fa169056168939a8b0b28eafe0d724f18dc4a7

strHex:

encTxt:452f12f4712f4c769a75b33cb995fa169056168939a8b0b28eafe0d724f18dc4a7


Flag Collection:

{

`        `apiKey: "AIzaSyDHjPh1vkUeGy37mS3cHn-D1UU\_oipuTYY",

`        `authDomain: "vishwactf-challenge12.firebaseapp.com",

`        `projectId: "vishwactf-challenge12",

`        `storageBucket: "vishwactf-challenge12.appspot.com",

`        `messagingSenderId: "435590274737",

`        `appId: "1:435590274737:web:2bfab4663703ba42c40c90",

`        `databaseURL:"https://vishwa-ctf-default-rtdb.firebaseio.com"

`      `};

