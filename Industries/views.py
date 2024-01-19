from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create(request):
    try:
        industry_name = request.data['industry_name']
        if Industries.objects.filter(industry_name=industry_name).exists():
            return Response({"message":"Already Exists","status":400,"data":[], "errors":"Industry already exists"})
        else:
            serializer = IndustriesSerializer(data=request.data)
            if serializer.is_valid():
                industry = serializer.save()
                return Response({"message":"Success", "status":200, "data":[IndustriesSerializer(industry).data], "errors":""})
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
        industry_name = request.data['industry_name']
        if Industries.objects.filter(industry_name=industry_name).exclude(id=id).exists():
            return Response({"message":"Already Exists","status":400,"data":[], "errors":"Industry already exists"})
        else:
            if Industries.objects.filter(id=id).exists():
                industry_obj = Industries.objects.filter(id=id).first()
                request.data['update_at'] = ''
                serializer = IndustriesSerializer(instance=industry_obj, data=request.data, partial=True)
                if serializer.is_valid():
                    industry = serializer.save()
                    return Response({"message":"Success", "status":200, "data":[IndustriesSerializer(industry).data], "errors":""})
                else:
                    first_error = next(iter(serializer.errors.values()))
                    return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)}) 
            else:
                return Response({"message":"Not Found","status":404,"data":[], "errors":"Industry data not found"})       
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)})    
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all(request):
    try:
        if Industries.objects.all().exists():
            app_objs = Industries.objects.all().order_by('industry_name')
            serializer = IndustriesSerializer(app_objs, many=True)            
            return Response({"message":"Success", "status":200, "data":serializer.data, "errors":""})         
        else:
            return Response({"message":"Not Found","status":404,"data":[], "errors":"Industry data not found"})       
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)}) 
