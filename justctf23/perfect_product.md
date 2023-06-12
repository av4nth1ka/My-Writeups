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
If we include a malicious payload in the request parameters, they can manipulate the `params` objects and modify the prototype

