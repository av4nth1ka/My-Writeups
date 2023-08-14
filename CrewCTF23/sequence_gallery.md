Important:
+ dc command in Linux is used to evaluate arithmetic expressions. It evaluates expressions in the form of a postfix expression. Entering a number pushes it into the stack and entering an operator evaluates an expression and pushes the result back into the stack. It can evaluate +, -, /, *, %, ^
+ In route /, when the sequence GET parameter is given, it'll strip out all rest of the path and ONLY extract the filename. Then, it'll append .dc to the filename. For example, parameter value power will become power.dc.
Moreover, if the sequence GET parameter's value contains a space character () or flag, it'll return :(.
+ Our sequence GET parameter's value is being parsed as an argument in the dc command, thus it's very likely to be vulnerable to argument injection:
![image](https://github.com/Avanthikaanand/My-Writeups/assets/80388135/c33113c4-7e7e-4bd6-8b46-e03bacc85680)
Yes now its confirmed that it is vulnerable to argument injection
+ While reading man page of the dc command we found this:
![image](https://github.com/Avanthikaanand/My-Writeups/assets/80388135/34ea0e1d-dc6b-47fa-9b16-2dc9f56b1884)
+ ![image](https://github.com/Avanthikaanand/My-Writeups/assets/80388135/afa21f49-41a7-45d5-9957-e136cc9ffc66)
In order to bypass the space character filter, we can try to replace the space character with anything else
Still the id didnt get executed.
`-e"!id%0a`
This is because our id command hasn't pressed the Enter key, or the new line character \n (%0a in URL encoding)
+ In Bash, we can use the $IFS special shell variable. The $IFS (Internal Field Separator) is used by the shell to determine how to do word splitting, the default value for $IFS consists of whitespace characters.
Next, we need to bypass the flag filter.
To do so, we can use the * wildcard character, which will then read all the files in the current working directory.
Hence, the final payload will be:<br>
`-e"!cat$IFS*.txt%0A`
Thus we get the flag

Original writeup:
https://ctftime.org/writeup/37413

Reference:
+ https://linux.die.net/man/1/dc
+ https://www.tutorialspoint.com/the-meaning-of-ifs-in-bash-scripting-on-linux
