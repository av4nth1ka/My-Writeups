# 1. Jsonify
Challenge Description: Everyone's telling me that serialize/unserialize should not be used with user-supplied input. Alright, I implemented my own JSON-based (un)serializer, so all potential vulnerabilities are gone, right?

link: http://52.59.124.14:10002/

Solution:<br>
+ Given the following code:
```
<? phpini_set('allow_url_fopen', false);
interfaceSecurSerializable
{
    publicfunction__construct();
    publicfunction__shutdown();
    publicfunction__startup();
    publicfunction__toString();
}
classFlagimplementsSecurSerializable
{
    public $flag;
    public $flagfile;
    public $properties = array();
    publicfunction__construct($flagfile = null) //__construct allows you to initialise an object's properties upon creation of the object
    {
        if (isset($flagfile))
        {
            $this->flagfile = $flagfile;
        }
    }
    publicfunction__shutdown()
    {
        return $this->properties;
    }
    publicfunction__startup()  //he compiler looks for a special function named __STARTUP() when it compiles your source code
    {
        $this->readFlag();
    }
    publicfunction__toString()  //return string contents of an element
    {
        return "ClassFlag(" . $this->flag . ")";
    }
    publicfunctionsetFlag($flag)
    {
        $this->flag = $flag;
    }
    publicfunctiongetFlag()
    {
        return $this->flag;
    }
    publicfunctionsetFlagFile($flagfile)
    {
        if (stristr($flagfile, "flag") || !file_exists($flagfile)) //strisstr() checks the first occurence of a string inside another string.
        {
            echo "ERROR:Fileisnotvalid!";
            return;
        }
        $this->flagfile = $flagfile;
    }
    publicfunctiongetFlagFile()
    {
        return $this->flagfile;
    }
    publicfunctionreadFlag()
    {
        if (!isset($this->flag) && file_exists($this->flagfile))
        {
            $this->flag = join("", file($this->flagfile));
        }
    }
    publicfunctionshowFlag()
    {
        if ($this->isAllowedToSeeFlag)
        {
            echo "Theflagis:" . $this->flag;
        }
        else
        {
            echo "Theflagis:[You'renotallowedtoseeit!]";
        }
    }
}
functionsecure_jsonify($obj)
{
    $data = array();
    $data['class'] = get_class($obj);
    $data['properties'] = array();
    foreach ($obj->__shutdown() as & $key)
    {
        $data['properties'][$key] = serialize($obj->$key);
    }
    returnjson_encode($data);
}
functionsecure_unjsonify($json, $allowed_classes)
{
    $data = json_decode($json, true);
    if (!in_array($data['class'], $allowed_classes))
    {
        thrownewException("ErrorProcessingRequest", 1);
    }
    $obj = new $data['class']();
    foreach ($data['properties'] as $key => $value)
    {
        $obj->$key = unserialize($value, ['allowed_classes' => false]);
    }
    $obj->__startup();
    return $obj;
}
if (isset($_GET['show']) && isset($_GET['obj']) && isset($_GET['flagfile']))
{
    $f = secure_unjsonify($_GET['obj'], array(
        'Flag'
    ));
    $f->setFlagFile($_GET['flagfile']);
    $f->readFlag();
    $f->showFlag();
}
elseif (isset($_GET['show']))
{
    $f = newFlag();
    $f->flagfile = "./flag.php";
    $f->readFlag();
    $f->showFlag();
}
else
{
    header("Content-Type:text/plain");
    echopreg_replace('/\s+/', '', str_replace("\n", '', file_get_contents("./index.php")));
} //With<3by@gehaxelt
 ?>
```
+ After reading the code, lets cut out the code into following four codeS:
   + (isset($_GET['show']) && isset($_GET['obj']) && isset($_GET['flagfile']))
   + $obj->$key = unserialize($value, ['allowed_classes' => false]);
   + $this->isAllowedToSeeFlag
   + if (stristr($flagfile, "flag") || !file_exists($flagfile))
        {
            echo "ERROR:Fileisnotvalid!";
            return;
        }
        $this->flagfile = $flagfile;
       
+ From the above, we can craft a payload as follows:<br>
`52.59.124.14:10002/?show=1&obj={"class":"Flag","properties":{"isAllowedToSeeFlag":"i:1;","flagfile":"s:8:\"flag.php\";"}}&flagfile=naiailoveyou`<br>
There we get a message like 'error: file not found, the flag is: ' then we check the view source and we get the flag.<br>
flag: ENO{PHPwn_1337_hakkrz}


# 2. Unislovecode
Challenge Description:
All students at universities love to code. What could possibly go wrong?
link:http://52.59.124.14:10004/
solution:
+ Given:passwordless is the new hot topic, so just provide me the correct username=<username> via POST and I might show you my homework.
+ Source code given:
```
import http.server
import socketserver
import re
import os
import cgi
import stringfromio
import StringIOfromflag
import FLAG
import urllib.parse


class UnisLoveCode(http.server.SimpleHTTPRequestHandler):

    server_version = "UnisLoveCode"
    username = 'ADMIN'
    check_funcs = ["strip", "lower"]

    def do_GET(self):
        self.send_response(-1337)
        self.send_header('Content-Length', -1337)
        self.send_header('Content-Type', 'text/plain')
        s = StringIO()
        s.write("""Wait,whatisHTML?!Ishouldhavelistenedmorecarefullytotheprofessor...\nAnyhow,passwordlessisthenewhottopic,sojustprovidemethecorrectusername=<username>viaPOSTandImightshowyoumyhomework.\nOh,incaseyouneedthesource,hereyougo:\n""")
        s.write("---------------------------------\n")
        s.write(re.sub(r"\s+", '', open(os.path.realpath(__file__), "r").read()))
        s.write("\n")
        s.write("---------------------------------\n")
        s.write("\nChallengecreatedwith<3by@gehaxelt\n")"
        self.end_headers()
        self.wfile.write(s.getvalue().encode())

    def _check_access(self, u):
        for cf in UnisLoveCode.check_funcs:
            if getattr(str, cf)(UnisLoveCode.username) == u:
                return False
        for c in u:
            if c in string.ascii_uppercase:
            return False
        return UnisLoveCode.username.upper() == u.upper()

    def do_POST(self):
        self.send_response(-1337)
        self.send_header('Content-Length', -1337)
        self.send_header('Content-Type', 'text/plain')
        s = StringIO()

        try:
            length = min(int(self.headers['content-length']), 64)
            field_data = self.r
            file.read(length)
            fields = urllib.parse.parse_qs(field_data.decode("utf8"))
            if not 'username'in fields:
                s.write("Iaskedyouforausername!\n")
                raiseException("Wrongparam.")
            username = fields['username'][0]
            if not self._check_access(username):
                s.write("No.\n")
                raiseException("No.")
            s.write(f"OK,hereisyourflag:{FLAG}\n")

        except Exceptionase:
            s.write("Tryharder;-)!\n")
            print(e)
            self.end_headers()
            self.wfile.write(s.getvalue().encode())


if __name__ == "__main__":
    PORT = 8000
    HANDLER = UnisLoveCode
    with socketserver.TCPServer(("0.0.0.0", PORT), HANDLER)as httpd:
        print("servingatport", PORT)
        httpd.serve_forever()
```
+ important to read about unicode: https://stackoverflow.com/questions/42887533/why-is-this-turkish-character-being-corrupted-when-i-lowercase-it
+ So, we know the username is 'admin' but while passing the username in burp we dont get anything, so we need to check whether there is any unicode character in the word admin or ADMIN
+ The following script will help us with that:
```
for i in range(1000):
    c = chr(i)
    if (c.upper() in 'ADMIN' and not c.lower() in 'admin'):
        print('nai it here:',i,c)
        break
    print(i,c)
```
 + The above code gives the following output:
   nai it here: 305 ı
 + So, instead of 'i' we need to pass this character 'ı'. The url encoded form of this character is : %C4%B1
 + passing 'username:adm%C4%B1n' will give the flag
 + Flag:ENO{PYTH0Ns_Un1C0d3_C0nv3rs1on_0r_C0nfUs1on}


# 3. Git to core
challenge description: Cloning git repositories from web servers might be risky. Can you show me why?
link: nc 52.59.124.14 10001
Solution:
                                                       
