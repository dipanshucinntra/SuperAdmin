from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from Services.other_services import Link_Generator
from .serializers import *
from .models import *

# Create your views here.
@api_view(['POST'])
def create(request):
    try:
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            return Response({"message":"Unsuccess","status":201,"data":[]})
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Success", "status":200,"data":[]})
            else:
                first_error = next(iter(serializer.errors.values()))
                print(f"First error: {first_error}")  
                return Response({"message":"Unsuccess","status":201,"data":[], "error":str(first_error)})     
    except Exception as e:
        return Response({"message":"Unsuccess","status":201,"data":[], "error":str(e)})  

@api_view(['POST'])
def login(request):
    try:
        email = request.data['email']
        password = request.data['password']
        if User.objects.filter(email=email).exists():
            user_obj = authenticate(request, email=email, password=password) 
            if user_obj is not None:
                token = Token.objects.create(user=user_obj)
                return Response({"message":"Success","status":201,"data":[{"token":token.key}]})
            else:
                return Response({"message":"Unauthorized","status":401,"data":[], "error":"Invaild Email or Password"})  
        else:
            return Response({"message":"Invalid User","status":403,"data":[], "error":""})   
    except Exception as e:
        return Response({"message":"Unsuccess","status":201,"data":[], "error":str(e)})     

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    try:
        id = request.data['id']
        email = request.data['email']
        if User.objects.filter(email=email).exclude(id=id).exists():
            return Response({"message":"Unsuccess","status":201,"data":[]})
        else:
            user_obj = User.objects.filter(id=id).first()
            serializer = UserSerializer(instance=user_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Success", "status":200,"data":[]})
            else:
                first_error = next(iter(serializer.errors.values()))
                print(f"First error: {first_error}")  
                return Response({"message":"Unsuccess","status":201,"data":[], "error":str(first_error)})     
    except Exception as e:
        return Response({"message":"Unsuccess","status":201,"data":[], "error":str(e)})   

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detail(request):
    try:
        id = request.data['id']       
        if User.objects.filter(id=id).exists():
            user_obj = User.objects.filter(id=id).first()
            serializer = UserSerializer(user_obj, many=True)            
            return Response({"message":"Success", "status":200,"data":serializer.data})
        else:
            return Response({"message":"Not Found","status":201,"data":[], "error":"User details not found"})     
    except Exception as e:
        return Response({"message":"Unsuccess","status":201,"data":[], "error":str(e)}) 

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])        
def password_change(request):
    try: 
        data = request.data
        serializer = PasswordChangeSerializer(data =data, context={'user':request.user})  
        if serializer.is_valid(raise_exception=True):       
            return Response({"message":"Your password changed successfully", "status":200, "data":[]}) 
        return Response(str(serializer.errors), status=400)
    except Exception as e:
        return Response({"message":"Unsuccess","status":201,"data":[], "error":str(e)}) 

@api_view(['POST'])       
def forgot_password_link(request):
    try:
        data = request.data
        email = data['email']  
        if User.objects.filter(email=email).exists:
            serializer = PasswordForgotLinkSerializer(data=request.data)
            if serializer.is_valid():                
                print("serializer :", serializer.data)
            return Response({"msg":"Password Reset link generated", "data":[], "status":200}) 
        else:
            return Response({"message":"Not Found","status":201,"data":[], "error":"User details not found"})  
    except Exception as e:
        return Response({"message":"Unsuccess","status":201,"data":[], "error":str(e)})     
    
    
@api_view(['POST'])       
def forgot_password(request, uid, token,):
    try:
        serializer = PasswordForgotSerializer(data=request.data, context={"uid":uid, "token":token})  
        if serializer.is_valid(raise_exception=True):  
            return Response({"message":"Password Rest Successfully"}, status=200) 
        return Response(str(serializer.errors), status=400)   
    except Exception as e:
        return Response({"message":"Unsuccess","status":201,"data":[], "error":str(e)})     

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Revoke or delete the authentication token
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # or use token.revoke() if you have django-rest-framework-authtoken >= 2.0.0
        except Token.DoesNotExist as e:
            # Token not found, no action needed
            return Response({"message":"User is not authenticated","status":201,"data":[], "error":str(e)})    
        # Perform regular logout
        logout(request)
        return Response({'message': 'Logout successful'})
    else:
        return Response({'message': 'User is not authenticated'})

