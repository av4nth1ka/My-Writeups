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
