description: I think this JWT implementation is not bad.

What is a JWT?
![image](https://github.com/av4nth1ka/My-Writeups/assets/80388135/c7ad2cc4-3b2d-4110-b248-1992d5601a39)
In this challenge, we are given with the code of index.js and jwt.js. From this part of index.js we can understand that we need to produce a jwt token which makes `isAdmin=true`
![image](https://github.com/av4nth1ka/My-Writeups/assets/80388135/11f22b0f-d951-4c30-a0c6-23e8999c01bb)
```
const algorithms = {
  hs256: (data, secret) => 
    base64UrlEncode(crypto.createHmac('sha256', secret).update(data).digest()),
  hs512: (data, secret) => 
    base64UrlEncode(crypto.createHmac('sha512', secret).update(data).digest()),
}

const createSignature = (header, payload, secret) => {
  const data = `${stringifyPart(header)}.${stringifyPart(payload)}`;
  const signature = algorithms[header.alg.toLowerCase()](data, secret);
  return signature;
}
```
+ If header.alg is constructor, it becomes const signature = Object(data,secret), and the resulting signature becomes a string object that only contains data, ignoring the secret:
