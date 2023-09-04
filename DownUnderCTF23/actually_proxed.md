The proxy will request the x-forwarded-for header value with the actual client ip, therefore we cannot use the same exploit as in the previous challenge. But the proxy code breaks after the first found occurrence of x-forwarded-for meaning, we can just pass multiple spoofed x-forwarded-for headers, the first will be replaced, but all others are kept intact. Since the last occurence is considered when calling request.Header.Values("X-Forwarded-For") we still can spoof the ip address.

$ curl http://actually.proxed.duc.tf:30009/ -H "X-Forwarded-For: 1337" -H "X-Forwarded-For: 31.33.33.7"
