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
        print("request data : ", request.data)
        application_details = request.data['application_details']
        customer_name = request.data['customer_name']
        if Customer.objects.filter(customer_name=customer_name).exists():
            return Response({"message":"Already Exists","status":400,"data":[], "errors":"Customer is already exists"})
        else: 
            industry_id = request.data['industry']    
            try:
                industry_obj = Industries.objects.filter(id=industry_id).first()
                request.data['industry'] = IndustriesSerializer(industry_obj).data
            except Industries.DoesNotExist:
                return Response({"message": "Not Found", "status": 404, "data": [], "errors": "Industry not found"})                   
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                customer = serializer.save()
                try:
                    print("customer industry : ", customer.industry)
                    for application in application_details: 
                        application_id = application['application']                                               
                        application_obj = Application.objects.filter(id=application_id).first()
                        application['application']= [ApplicationSerializer(application_obj).data]
                        customer_dict = CustomerDetailsSerializer(customer).data
                        customer_dict['industry'] = IndustriesSerializer(customer.industry).data
                        application['customer'] = customer_dict
                except Application.DoesNotExist:
                    return Response({"message": "Not Found", "status": 404, "data": [], "errors": "Application not found"})  
                app_serializer = ApplicationDetailsSerializer(data=application_details, many=True)
                if app_serializer.is_valid():
                    app_objs = app_serializer.save()
                    return Response({"message":"Success", "status":200, "data":app_serializer.data, "errors":""})
                else:
                    customer_id = customer.id
                    if ApplicationDetails.objects.filter(customer=customer).exists():
                       ApplicationDetails.objects.filter(customer=customer).delete() 
                    if Customer.objects.filter(id=customer_id).exists():
                       Customer.objects.filter(id=customer_id).delete() 
                    # first_error = next(iter(app_serializer.errors.values()))
                    return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(app_serializer.errors)})                         
            else:
                # first_error = next(iter(serializer.errors.values()))
                return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(serializer.errors)})   
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


