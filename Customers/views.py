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
        customer_name = request.data['customer_name']
        if Customer.objects.filter(customer_name=customer_name).exists():
            return Response({"message":"Already Exists","status":400,"data":[], "errors":"Application already exists"})
        else:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                customer = serializer.save()
                app_serializer = ApplicationDetailsSerializer(data=request.data['applications'])
                if app_serializer.is_valid():
                    app_obj = app_serializer.save()
                    return Response({"message":"Success", "status":200, "data":[ApplicationDetailsSerializer(app_obj).data], "errors":""})
                else:
                    customer_id = customer.id
                    if ApplicationDetails.objects.filter(customer=customer).exists():
                       ApplicationDetails.objects.filter(customer=customer).delete() 
                    if Customer.objects.filter(id=customer_id).exists():
                       Customer.objects.filter(id=customer_id).delete() 
                    first_error = next(iter(serializer.errors.values()))
                    return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)})
            else:
                first_error = next(iter(serializer.errors.values()))
                return Response({"message":"Unsuccess","status":403,"data":[], "errors":str(first_error)})   
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


