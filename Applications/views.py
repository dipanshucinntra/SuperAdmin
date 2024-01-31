from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db.models import Q
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

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detail(request):
    try:
        id = request.data['id']
        if Application.objects.filter(id=id).exists():
            app_objs = Application.objects.filter(id=id)
            serializer = ApplicationSerializer(app_objs, many=True)            
            return Response({"message":"Success", "status":200, "data":serializer.data, "errors":""})         
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
            app_objs = Application.objects.all().order_by('id') #application_name
            serializer = ApplicationSerializer(app_objs, many=True)            
            return Response({"message":"Success", "status":200, "data":serializer.data, "errors":""})         
        else:
            return Response({"message":"Not Found","status":403,"data":[], "errors":"Application data not found"})       
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)}) 


# @api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def all_filter_page(request):
#     try:
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         json_data       = request.data
#         leadType        = request.data['leadType']
#         SearchText      = json_data['SearchText']
#         order_by_field  = json_data['order_by_field']
#         order_by_value  = json_data['order_by_value']
#         page            = settings.PAGE(json_data)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         orderby = "-id"
#         if str(order_by_field).strip() != "":
#             orderby = f"{order_by_field}"
#             if str(order_by_value).lower() == 'desc':
#                 orderby = f"-{order_by_field}"        
#             app_obj = Application.objects.filter(**json_data['field']).order_by(orderby)            
#             # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#             if str(app_obj) != "":
#                 leads_obj = leads_obj.filter( 
#                     Q(pk__icontains = SearchText) | 
#                     Q(location__icontains = SearchText) | 
#                     Q(companyName__icontains = SearchText) | 
#                     Q(contactPerson__icontains = SearchText) | 
#                     Q(phoneNumber__icontains = SearchText) | 
#                     Q(source__icontains = SearchText) | 
#                     Q(leadType__icontains = SearchText) | 
#                     Q(status__icontains = SearchText) | 
#                     Q(email__icontains = SearchText)
#                 ).order_by(orderby)
#             print(leads_obj.query)
#             # end if 
#             # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#             count = leads_obj.count()
#             leads_obj = leads_obj[page['startWith']:page['endWith']]   
#             # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#             leads_json = ApplicationSerializer(leads_obj, many = True)
#             # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#             return Response({"message": "Success","status": 200,"data":leads_json.data, "meta":{"count":count}})
#         else:
#             return Response({"message": "Invalid SalesEmployeeCode?", "status": 201, "data":[]})
#     except Exception as e:
#             return Response({"message": str(e), "status": 201, "data":[]})