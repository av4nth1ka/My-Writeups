#deno #ssrf #lfi


Important:
+ Deno is a runtime for JavaScript, TypeScript, and WebAssembly that is based on the V8 JavaScript engine and the Rust programming language.
+ Oak is a middleware framework for handling HTTP with Deno.
+ Explanation of main.js :
```
The code revokes the net permission from the Deno permissions using await Deno.permissions.revoke({ name: 'net', host: PROVIDER_HOST }). This step is done to ensure that there's no potential for Server-Side Request Forgery (SSRF) attacks using this endpoint.
The code sets up routes using the Oak Router. It defines two routes:

The root route '/' handles the main functionality of calculating the hash of the fetched FLAG and rendering it in an HTML template.
The /proxy route is a simple proxy that fetches content from URLs specified in the query parameter url.
```
+ The main.js is run as follows:
  deno run --no-prompt --allow-net="0.0.0.0:8080,$PROVIDER_HOST" --allow-read=. --allow-env ./main.js
+ it allows the script to listen on a specific network address, read files from the current directory, access environment variables, and make network requests to the specified addresses, that is itself and the flag provider which is a service that is exposed only in the internal network
+ From the main.js in the flag provider, If the token matches the PROVIDER_TOKEN loaded from the environment variable, the response body is set to a string containing FLAG.
+ In the main.js in the source, the `fetch()` function takes unsanitised input.
+ Given the very restricted scope of reachable endpoints, we began looking for other URI schemes the Deno fetch implementation supports, and we stumbled upon this, which made us think about trying to perform an LFI attack.
+ To test for it, we tried navigating to http://safe-proxy-web.chal.crewc.tf:8083/proxy?url=file:///home/app/main.js. We got back the file main.js, thus confirming the possibility of LFI.
+ tried to understand where Deno stores relevant files
+ https://denolib.gitbook.io/guide/advanced/deno_dir-code-fetch-and-cache
+ $DENO_DIR/deps is used to store files fetched through remote url import. It contains subfolders based on url scheme (currently only http and https), and store files to locations based on the URL path. Since the application loads the flag by using import, we thought about trying to use fetch to include the file created in the deps directory at import time.
+ Locally in .cache/deno directory,We noticed that the deps folder contains the imported modules in files whose names are hashes (presumably SHA-256 hashes), hence to import the right file we needed to know what’s the right hash for it
+ try and compute the hash of the path used for importing the flag, that is http://${PROVIDER_HOST}/?token=${PROVIDER_TOKEN}.
+ in the .cache/deno folder there’s a file called dep_analysis_cache_v1 that seems to be a database storing information about the imported modules. This file contains the full url used when making the request, thus leaking the token, that is 5a35327045b0ec9159cc188f643e347f.
+ We replaced the redacted PROVIDER_TOKEN in the Dockerfile with the real one, and we built and ran the containers again
+ The full path is: /home/app/.cache/deno/deps/http/safe-proxy-flag-provider_PORT8082/70ec621b0141f80c80d9e26b084da38df4bbf6b4b64d04c837f7b3cd5fe8482b
Passing this path in the url parameter to /proxy, we get the flag back

Good writeup:

https://untrue.me/writeups/crewctf2023/safe-proxy/
