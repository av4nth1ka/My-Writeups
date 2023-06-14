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

