from logging import log
from Applications.serializers import ApplicationSerializer
from Industries.serializers import IndustriesSerializer
from rest_framework import serializers
from .models import *

class CustomerDetailsSerializer(serializers.ModelSerializer): 
    application_details = serializers.SerializerMethodField('get_application_details')
    industry_details = serializers.SerializerMethodField('get_industry_details')
    class Meta:
        model = Customer
        fields = '__all__'
        extra_fields = ['application_details', 'industry_details']  

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

    def get_industry_details(self, obj):
        try:
            if Industries.objects.filter(id=obj.industry_id).exists():
               objs = Industries.objects.filter(id=obj.industry_id) 
               serializer = IndustriesSerializer(objs, many=True)
               return serializer.data
            else:
                return []
        except Exception as e:
            return str(e) 

class CustomerWithIndustriesSerializer(serializers.ModelSerializer): 
    industry_details = serializers.SerializerMethodField('get_industry_details')
    class Meta:
        model = Customer
        fields = '__all__'
        extra_fields = ['industry_details']    

    def get_industry_details(self, obj):
        try:
            if Industries.objects.filter(id=obj.industry_id).exists():
               objs = Industries.objects.filter(id=obj.industry_id) 
               serializer = IndustriesSerializer(objs, many=True)
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
    

class ApplicationDetailsListSerializer(serializers.ModelSerializer):
    application_info = serializers.SerializerMethodField('get_application_info')
    customer_details = serializers.SerializerMethodField('get_customer_details')
    class Meta:
        model = ApplicationDetails
        fields = '__all__' 
        extra_fields=["application_info", "customer_details"]
        
    def get_application_info(self, obj):
        try:
            if Application.objects.filter(id=obj.application_id).exists():
               objs = Application.objects.filter(id=obj.application_id) 
               serializer = ApplicationSerializer(objs, many=True)
               return serializer.data
            else:
                return []
        except Exception as e:
            return str(e) 

    def get_customer_details(self, obj):
        try:
            if Customer.objects.filter(id=obj.customer_id).exists():
               objs = Customer.objects.filter(id=obj.customer_id) 
               serializer = CustomerWithIndustriesSerializer(objs, many=True)
               return serializer.data
            else:
                return []
        except Exception as e:
            return str(e)
