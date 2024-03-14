PICOCTF 2022

Writeups

1. SECRETS:

Description: We have several pages hidden. Can you find the one with the flag?

The website is running [here](http://saturn.picoctf.net:50167/).

Solution:

- Here we inspect each page and visit the files given in the source.
- When inspecting the &#39;about&#39; section of the page, we found &quot;secret/assets/index.css&quot;.
- So, we went to [http://saturn.picoctf.net:50167/secret](http://saturn.picoctf.net:50167/secrets) and found another page with some image. When we inspected that particular page, we found &quot;hidden/file.css&quot;.
- Then we went to [http://saturn.picoctf.net:50167/secret/hidden](http://saturn.picoctf.net:50167/hidden) and found a new page. Inspected that file as well. Then we got &quot;superhidden/login.css&quot;. Then we went to [http://saturn.picoctf.net:50167/secret/hidden/superhidden](http://saturn.picoctf.net:50167/secret/hidden/superhidden) and found the flag while viewing the source of that page.
- Flag: **picoCTF{spicoCTF{succ3ss\_@h3n1c@10n\_51b260fe}ucc3ss\_@h3n1c@10n\_51b260fe}**

1. SQLi Lite:

- Description: Can you login to this website?

Try to login [here](http://saturn.picoctf.net:57561/).

- We can see a login page. When i gave

Username: admin

Password: admin

It gave the following message:

username: admin

password: admin

SQL query: SELECT \* FROM users WHERE name=&#39;admin&#39; AND password=&#39;admin&#39;

Login Failed.

- So, we can try injecting queries to get the flag
- I gave username: &#39; or 1=1 - - +
- Password as any random thing or even we can put it blank as we comment out the rest of the query.
- I got the following message:

username: &#39; or 1=1 --+

password:

SQL query: SELECT \* FROM users WHERE name=&#39;&#39; or 1=1 --+&#39; AND password=&#39;&#39;

# Logged in! But can you see the flag, it is in plain sight.

- When we view the page source we got the flag
- Flag: **picoCTF{L00k5\_l1k3\_y0u\_solv3d\_it\_d3c660ac}**

1. Roboto Sans:

- Description:The flag is somewhere on this web application not necessarily on the website. Find it.
- solution:
- When we went to /robots.txt, we found out the following

User-agent \*

Disallow: /cgi-bin/

Think you have seen your flag or want to keep looking.

ZmxhZzEudHh0;anMvbXlmaW

anMvbXlmaWxlLnR4dA==

svssshjweuiwl;oiho.bsvdaslejg

Disallow: /wp-admin/

- When I base64 decoded anMvbXlmaWxlLnR4dA== we got js/myfile.txt
- When we went to http://saturn.picoctf.net:51108/js/myfile.txt

we found the flag.

- picoCTF{Who\_D03sN7\_L1k5\_90B0T5\_22ce1f22}

1. SQL Direct:

- Description: Connect to this PostgreSQL server and find the flag!
- psql -h saturn.picoctf.net -p 55747 -U postgres pico
- Password is postgres

Solution:

- Installed Postgre sql
- Obtained the flag from a table named flag.

![](RackMultipart20220414-4-14v9kuj_html_ac5318c0dd5d4033.jpg)

Flag: picoCTF{L3arN\_S0m3\_5qL\_t0d4Y\_73b0678f}

NOTED:

- Description: I made a nice web app that lets you take notes. I&#39;m pretty sure I&#39;ve followed all the best practices so its definitely secure right?
- [http://saturn.picoctf.net:54558/](http://saturn.picoctf.net:54558/)
- Tried checking for xss in the page by creating a note.
- \&lt;script\&gt;alert(1)\&lt;/script\&gt;
- We are given with the source code.
- report.js:

async function run(url) {

let browser;

try {

module.exports.open = true;

browser = await puppeteer.launch({

headless: true,

pipe: true,

args: [&#39;--incognito&#39;, &#39;--no-sandbox&#39;, &#39;--disable-setuid-sandbox&#39;],

slowMo: 10

});

let page = (await browser.pages())[0]

await page.goto(&#39;http://0.0.0.0:8080/register&#39;);

await page.type(&#39;[name=&quot;username&quot;]&#39;, crypto.randomBytes(8).toString(&#39;hex&#39;));

await page.type(&#39;[name=&quot;password&quot;]&#39;, crypto.randomBytes(8).toString(&#39;hex&#39;));

await Promise.all([

page.click(&#39;[type=&quot;submit&quot;]&#39;),

page.waitForNavigation({ waituntil: &#39;domcontentloaded&#39; })

]);

await page.goto(&#39;http://0.0.0.0:8080/new&#39;);

await page.type(&#39;[name=&quot;title&quot;]&#39;, &#39;flag&#39;);

await page.type(&#39;[name=&quot;content&quot;]&#39;, process.env.flag ?? &#39;ctf{flag}&#39;);

await Promise.all([

page.click(&#39;[type=&quot;submit&quot;]&#39;),

page.waitForNavigation({ waituntil: &#39;domcontentloaded&#39; })

]);

await page.goto(&#39;about:blank&#39;)

await page.goto(url);

await page.waitForTimeout(7500);

await browser.close();

} catch(e) {

console.error(e);

try { await browser.close() } catch(e) {}

}

module.exports.open = false;

}

- We need to read the &quot;my notes&quot; from the bots account to get the flag
- The bot used here is a puppeteer bot
- [https://www.npmjs.com/package/puppeteer](https://www.npmjs.com/package/puppeteer)
-
