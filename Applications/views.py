from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create(request):
    try:
        application_name = request.data['application_name']
        if Application.objects.filter(application_name=application_name).exists():
            return Response({"message":"Already Exists","status":400,"data":[], "errors":"Application already exists"})
        else:
            serializer = ApplicationSerializer(data=request.data)
            if serializer.is_valid():
                app = serializer.save()
                return Response({"message":"Success", "status":200, "data":[ApplicationSerializer(app).data], "errors":""})
            else:
                first_error = next(iter(serializer.errors.values()))
                return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)})   
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)}) 
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    try:
        id = request.data['id']
        application_name = request.data['application_name']
        if Application.objects.filter(application_name=application_name).exclude(id=id).exists():
            return Response({"message":"Already Exists","status":400,"data":[], "errors":"Application already exists"})
        else:
            if Application.objects.filter(id=id).exists():
                app_obj = Application.objects.filter(id=id).first()
                request.data['update_at'] = ''
                serializer = ApplicationSerializer(instance=app_obj, data=request.data, partial=True)
                if serializer.is_valid():
                    app = serializer.save()
                    return Response({"message":"Success", "status":200, "data":[ApplicationSerializer(app).data], "errors":""})
                else:
                    first_error = next(iter(serializer.errors.values()))
                    return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)}) 
            else:
                return Response({"message":"Not Found","status":403,"data":[], "errors":"Application data not found"})       
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)})    
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all(request):
    try:
        if Application.objects.all().exists():
            app_objs = Application.objects.all().order_by('application_name')
            serializer = ApplicationSerializer(app_objs, many=True)            
            return Response({"message":"Success", "status":200, "data":serializer.data, "errors":""})         
        else:
            return Response({"message":"Not Found","status":403,"data":[], "errors":"Application data not found"})       
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)}) 