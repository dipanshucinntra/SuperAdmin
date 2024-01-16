from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def Link_Generator(user):     
    uid= urlsafe_base64_encode(force_bytes(user.id))
    print("Encoded user is: ", uid)
    token =PasswordResetTokenGenerator().make_token(user )
    print("Generated token: ", token)
    link ="/password_reset/"+uid+'/'+token
    print("Generated link: ", link)
    password_link=link
    return password_link