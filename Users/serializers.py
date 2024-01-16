from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from xml.dom import ValidationErr
from Services.Emailer import sendMail
from .models import *

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField() 
    password2 = serializers.CharField()
    class Meta:
        model = User
        fields = '__all__'
        required =True

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        print(attrs)
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password does't match")
        return attrs
    
    def create(self, validated_data):
        print("validating : ", validated_data)        
        return User.objects.create_user(**validated_data)    

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['email', 'password']       
    

class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True) 
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True) 
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        print(attrs)
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password does't match")
        user.set_password(password)
        user.save()
        return attrs

class UserPasswordForgotLink(serializers.Serializer):
    email = serializers.EmailField(max_length=255) 
    def validate(self, attrs):
        email = attrs.get('email')
        print(email)
        if User.objects.filter(email=email).exists:
            user = User.objects.get(email=email)
            uid= urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded user is: ", uid)
            token =PasswordResetTokenGenerator().make_token(user )
            print("Generated token: ", token)
            link ="http://127.0.0.1:9000/password_reset/"+uid+'/'+token
            print("Generated link: ", link)
            body="Click following link to reset password"+link            
            subject= "Rest Password" 
            to_email = email
            attachments =""
            sendMail(to_email, subject, body, attachments)
            return attrs
        else:
            raise ValidationErr("Your email address is not valid")

class UserPasswordForgot(serializers.Serializer):
    user =""
    token ="" 
    try:    
        password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True) 
        password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
        
        def validate(self, attrs):
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid= self.context.get('uid')
            token = self.context.get('token')
            print(attrs)
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password does't match")
            id =smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationErr("This link for password reset is invalid or expired")
            user.set_password(password)
            user.save()
            return attrs        
    except DjangoUnicodeDecodeError as e:
        PasswordResetTokenGenerator().check_token(user, token)
        raise  ValidationErr("This link for password reset is invalid or expired")



class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
         read_only_fields = ('id', 'is_active', 'is_staff')
    
    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass