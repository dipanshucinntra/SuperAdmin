from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def Link_Generator(user):     
    uid= urlsafe_base64_encode(force_bytes(user.id))
    token =PasswordResetTokenGenerator().make_token(user)
    link ="/password_reset/"+uid+'/'+token
    password_link=link
    return password_link