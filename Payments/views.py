from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from .serializers import *
from .models import *
import os

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create(request):
    try:        
        serializer = PyamentsHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            payment_id = PyamentsHistory.objects.latest("id").id
            for File in request.FILES.getlist('file'):
                file_url = ""
                if File !="" :
                    target ='./bridge/static/image/Attachment'
                    os.makedirs(target, exist_ok=True)
                    fss = FileSystemStorage()
                    file = fss.save(target+"/"+File.name, File)
                    productImage_url = fss.url(file)
                    file_url = productImage_url.replace('/bridge/', '/')
                    print(file_url)
                    file_serializer = AttachmentSerializer(data={"file_url":file_url, "link_id":payment_id, "link_type":"","caption":""})
                    if file_serializer.is_valid():
                        file_serializer.save()   
                    else:
                        if Attachment.objects.filter(link_id=payment_id).exists():
                           Attachment.objects.filter(link_id=payment_id).delete()
                        PyamentsHistory.objects.filter(id=payment_id).delete()    
                        first_error = next(iter(serializer.errors.values()))
                        return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)})                     
            return Response({"message":"Success", "status":200,"data":[], "errors":""})
        else:
            first_error = next(iter(serializer.errors.values()))
            return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)})     
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "errors":str(e)})  
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    try:  
        payment_id = request.data['payment_id']  
        if PyamentsHistory.objects.filter(id=payment_id).exists():
            history_obj = PyamentsHistory.objects.filter(id=payment_id).first()        
            serializer = PyamentsHistorySerializer(instance=history_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()                    
                return Response({"message":"Success", "status":200,"data":[], "errors":""})
            else:
                first_error = next(iter(serializer.errors.values()))
                return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)})  
        else:
            return Response({"message":"Not Found","status":403,"data":[], "errors":"Payment history your looking for is not found"})       
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "errors":str(e)})     
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def payment_detail(request):
    try:  
        payment_id = request.data['payment_id']  
        if PyamentsHistory.objects.filter(id=payment_id).exists():
            history_obj = PyamentsHistory.objects.filter(id=payment_id)        
            serializer = AttachPyamentsSerializer(history_obj, many=True)
            if serializer.is_valid():                                    
                return Response({"message":"Success", "status":200,"data":serializer.data, "errors":""})
            else:
                first_error = next(iter(serializer.errors.values()))
                return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)})  
        else:
            return Response({"message":"Not Found","status":403,"data":[], "errors":"Payment history your looking for is not found"})       
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "errors":str(e)})   
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def payment_list(request):
    try:  
        history_objs = PyamentsHistory.objects.all().order_by('-id')  
        if history_objs:       
            serializer = AttachPyamentsSerializer(history_objs, many=True)                                   
            return Response({"message":"Success", "status":200,"data":serializer.data, "errors":""})
        else:
            return Response({"message":"Not Found","status":403,"data":[], "errors":"Payment history your looking for is not found"})       
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "errors":str(e)})  