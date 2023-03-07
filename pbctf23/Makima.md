+ Two services: web and cdn (content delivery network)
+ In the webpage we are given with a field to upload image link
+ Upload source:
```
<?php
function makeimg($data, $imgPath, $mime) {
    $img = imagecreatefromstring($data);
    switch($mime){
        case 'image/png':
            $with_ext = $imgPath . '.png';
            imagepng($img, $with_ext);
            break;
        case 'image/jpeg':
            $with_ext = $imgPath . '.jpg';
            imagejpeg($img, $with_ext);
            break;
        case 'image/webp':
            $with_ext = $imgPath . '.webp';
            imagewebp($img, $with_ext);
            break;
        case 'image/gif':
            $with_ext = $imgPath . '.gif';
            imagegif($img, $with_ext);
            break;
        default:
            $with_ext = 0;
            break;
        }
    return $with_ext;
}

if(isset($_POST["url"])){ 
    $cdn_url = 'http://localhost:8080/cdn/' . $_POST["url"];
    $img = @file_get_contents($cdn_url);
    $f = finfo_open();
    $mime_type = finfo_buffer($f, $img, FILEINFO_MIME_TYPE);
    $fileName = 'uploads/' . substr(md5(rand()), 0, 13);
    $success = makeimg($img, $fileName, $mime_type);
    if ($success !== 0) {
        $msg = $success;
    }
} 
?>
```
This is a PHP script that receives a URL via a POST request and downloads an image from that URL to a local server directory called "uploads". The script then uses the "makeimg" function to create a new image file with a unique filename in the same directory, based on the file type of the downloaded image. The new image file is returned as the output of the script.
The "makeimg" function takes three parameters: $data, $imgPath, and $mime. $data is the image data to be used to create the new image file. $imgPath is the file path for the new image file. $mime is the MIME type of the image data. The function uses a switch statement to determine which PHP image function to use to create the new image file, based on the MIME type. The function returns the file path for the new image file.

+ cdn service source:
```
@app.route("/cdn/<path:url>")
def cdn(url):
    mimes = ["image/png", "image/jpeg", "image/gif", "image/webp"]
    r = requests.get(url, stream=True)
    if r.headers["Content-Type"] not in mimes:
        print("BAD MIME")
        return "????", 400
    img_resp = make_response(r.raw.read(), 200)
    for header in r.headers:
        if header == "Date" or header == "Server":
            continue
        img_resp.headers[header] = r.headers[header]
    return img_resp


if __name__ == "__main__":
    app.run(debug=False, port=8081)
```
When a GET request is made to the /cdn/path:url endpoint, the script uses the requests library to retrieve the image data from the specified URL
and checks if the Content-Type of the response matches one of the allowed MIME types for images (PNG, JPEG, GIF, and WebP).
If the Content-Type is valid, the script creates a Flask response object with the image data and sets the appropriate headers based on the original response from the URL. The response object is then returned to the client.

+ We can try controlling the image and response headers from the server.
+ As there is internal nginx directive, we cant access .php files from outside
+ `X-Accel Redirect` allows for internal redirection to a location determined by a header returned from a backend.
+ So inshort, it is possible to control the destination that nginx will redirect to , so we can set up the server to return the response headerX-Accel-Redirect: /uploads/<image_name>/bla.php
+ First we need to create a php shell and upload to the server.
+ 
