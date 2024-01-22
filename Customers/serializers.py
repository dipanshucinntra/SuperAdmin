from logging import log
from Applications.serializers import ApplicationSerializer
from Industries.serializers import IndustriesSerializer
from rest_framework import serializers
from .models import *

class CustomerDetailsSerializer(serializers.ModelSerializer): 
    application_details = serializers.SerializerMethodField('get_application_details')
    class Meta:
        model = Customer
        fields = '__all__'
        extra_fields = ['application_details']
        depth = 1  

    def get_application_details(self, obj):
        try:
            if ApplicationDetails.objects.filter(customer_id=obj.id).exists():
               objs = ApplicationDetails.objects.filter(customer_id=obj.id) 
               serializer = ApplicationDetailsSerializer(objs, many=True)
               return serializer.data
            else:
                return []
        except Exception as e:
            return str(e)    


class CustomerSerializer(serializers.ModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(queryset=Industries.objects.all())  
    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):  
        customer = Customer.objects.create(**validated_data) 
        return customer    

class EmployeeSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):        
         employee = Employee.objects.create(**validated_data)
         return employee   

class ApplicationDetailsSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    application = serializers.PrimaryKeyRelatedField(queryset=Application.objects.all())
    class Meta:
        model = ApplicationDetails
        fields = '__all__'

    def create(self, validated_data):        
         application_details = ApplicationDetails.objects.create(**validated_data)
         return application_details    
    


