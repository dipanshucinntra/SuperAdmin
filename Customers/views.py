from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create(request):
    try:
        customer_id = 0
        print("request data : ", request.data)
        application_details = request.data['application_details']
        customer_name = request.data['customer_name']
        if Customer.objects.filter(customer_name=customer_name).exists():
            return Response({"message":"Already Exists","status":400,"data":[], "errors":"Customer is already exists"})
        else:            
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                customer_id =Customer.objects.latest('id').id
                for app_obj in application_details:
                    app_obj['customer'] = customer_id
                print("application_details : ",application_details)    
                app_serializer = ApplicationDetailsSerializer(data=application_details, many=True)
                if app_serializer.is_valid():
                    app_serializer.save()
                    return Response({"message":"Success", "status":200, "data":app_serializer.data, "errors":""})
                else:
                    if ApplicationDetails.objects.filter(customer_id=customer_id).exists():
                       ApplicationDetails.objects.filter(customer_id=customer_id).delete() 
                    if Customer.objects.filter(id=customer_id).exists():
                       Customer.objects.filter(id=customer_id).delete() 
                    first_error = next(iter(app_serializer.errors.values()))
                    return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(app_serializer.errors), "from":"app serializer"})                         
            else:
                return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(serializer.errors), "from":"customer serializer"})   
    except Exception as e:
        if Customer.objects.filter(id=customer_id).exists():
            Customer.objects.filter(id=customer_id).delete() 
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    try:
        app_id_list=[]
        customer_id = request.data['id']
        application_details = request.data['application_details']
        customer_name = request.data['customer_name']
        if Customer.objects.filter(id=customer_id).exists():
            if Customer.objects.filter(customer_name=customer_name).exclude(id=customer_id).exists():
                return Response({"message":"Already Exists","status":400,"data":[], "errors":"Customer is already exists"})
            else: 
                customer_obj = Customer.objects.filter(id=customer_id).first()           
                serializer = CustomerSerializer(instance=customer_obj, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    customer_id =Customer.objects.latest('id').id
                    for app_obj in application_details:
                        app_id = app_obj['id'] if 'id' in app_obj and app_obj['id'] !="" else None
                        if app_id:
                            if ApplicationDetails.objects.filter(id=app_id).exists():
                                app_instance = ApplicationDetails.objects.filter(id=app_id).first()
                                app_serializer = ApplicationDetailsSerializer(instance=app_instance, data=app_obj, partial=True)
                                if app_serializer.is_valid():
                                    app_serializer.save()
                                    app_id_list.append(int(app_id))
                                else:
                                    first_error = next(iter(app_serializer.errors.values()))
                                    return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error), "from":"app old update serializer"})     
                            else:
                                return Response({"message":"Not Found","status":400,"data":[], "errors":"Application deatails were not founds"})   
                        else:                    
                            app_serializer = ApplicationDetailsSerializer(data=application_details, many=True)
                            if app_serializer.is_valid():
                                app_serializer.save()
                                app_id = ApplicationDetails.objects.latest('id').id
                                app_id_list.append(int(app_id))
                            else:
                                first_error = next(iter(app_serializer.errors.values()))
                                return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error), "from":"app new create serializer"})  
                    if app_id_list:
                        ApplicationDetails.objects.filter(customer_id=customer_id).exclude(id__in=app_id_list).delete()                                       
                    return Response({"message":"Success", "status":200, "data":[], "errors":""})                    
                else:
                    return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(serializer.errors), "from":"customer serializer"})   
        else:
            return Response({"message":"Not Found","status":400,"data":[], "errors":"Customer were not founds"})   
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)})
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detail(request):
    try:        
        customer_id = request.data['id']
        if Customer.objects.filter(id=customer_id).exists():
           customer_obj = Customer.objects.filter(id=customer_id)
           serializer = CustomerDetailsSerializer(customer_obj, many=True)
           return Response({"message":"Success", "status":200, "data":serializer.data, "errors":""}) 
        else: 
            return Response({"message":"Not Found","status":400,"data":[], "errors":"Customer were not founds"})            
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)})  

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all(request):
    try:        
        customer_objs = Customer.objects.all().order_by('-id')
        if customer_objs.exists():
           serializer = CustomerDetailsSerializer(customer_objs, many=True)
           return Response({"message":"Success", "status":200, "data":serializer.data, "errors":""}) 
        else: 
            return Response({"message":"Not Found","status":400,"data":[], "errors":"Customer were not founds"})            
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)})  
          

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_employee(request):
    try:
        email = request.data['email']
        if Employee.objects.filter(email=email).exists():
            return Response({"message":"Already Exists","status":400,"data":[], "errors":"Employee is already exists"})
        else:
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                emp_obj = serializer.save()
                return Response({"message":"Success", "status":200, "data":EmployeeSerializer(emp_obj).data, "errors":""})
            else:
                first_error = next(iter(serializer.errors.values()))
                return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)}) 
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_employee(request):
    try:
        email = request.data['email']
        emp_id = request.data['id']        
        if Employee.objects.filter(email=email).exclude(id=emp_id).exists():
            return Response({"message":"Already Exists","status":400,"data":[], "errors":"Employee is already exists"})
        else:
            if Employee.objects.filter(id=emp_id).exists():
                emp_obj= Employee.objects.filter(id=emp_id).first()
                serializer = EmployeeSerializer(instance=emp_obj, data=request.data, partial=True)
                if serializer.is_valid():
                    emp_obj = serializer.save()
                    return Response({"message":"Success", "status":200, "data":EmployeeSerializer(emp_obj).data, "errors":""})
                else:
                    first_error = next(iter(serializer.errors.values()))
                    return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)}) 
            else:
                return Response({"message":"Not Found","status":403,"data":[], "errors":"Employee is not exists"})    
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)})
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_emp_per_customer(request):
    try:        
        customer_id = request.data['customer_id']        
        if Employee.objects.filter(customer_id=customer_id).exists():
           emp_objs = Employee.objects.filter(customer_id=customer_id)
           serializer = EmployeeSerializer(emp_objs, many=True) 
           return Response({"message":"Success", "status":200, "data":serializer.data, "errors":""})    
        else:            
            return Response({"message":"Not Found","status":403,"data":[], "errors":"Employee is not exists"})    
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "error":str(e)})    

@api_view(['GET', 'POST'])
def customer_list(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a specific customer
@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





