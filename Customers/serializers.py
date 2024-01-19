from logging import log
from Applications.serializers import ApplicationSerializer
from Industries.serializers import IndustriesSerializer
from rest_framework import serializers
from .models import *

class CustomerDetailsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Customer
        fields = '__all__'
        

class CustomerSerializer(serializers.ModelSerializer):
    industry = IndustriesSerializer()    
    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data): 
        industry = validated_data.pop('industry')
        industry_instance, _ = Industries.objects.get_or_create(**industry) 
        customer = Customer.objects.create(industry=industry_instance, **validated_data)
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
    customer = CustomerSerializer()
    application = ApplicationSerializer(many=True)
    class Meta:
        model = ApplicationDetails
        fields = '__all__'
    def create(self, validated_data):
        try:
            customer_data = validated_data.pop('customer')
            customer_instance, _ = Customer.objects.get_or_create(**customer_data)
            applications_data = validated_data.pop('application')
            application_details_instance = ApplicationDetails.objects.create(customer=customer_instance, **validated_data)

            # Add the applications to the ManyToManyField
            for application_data in applications_data:
                application_instance, _ = Application.objects.get_or_create(**application_data)
                application_details_instance.application.add(application_instance)
            # log.debugg("application_details_instance :", application_details_instance)    
            return application_details_instance
        except Exception as e:
            return str(e)


# class ApplicationDetailsSerializer(serializers.ModelSerializer):
#     customer = CustomerSerializer()
#     application = ApplicationSerializer(many=True)

#     class Meta:
#         model = ApplicationDetails
#         fields = '__all__'

#     def create(self, validated_data):
#         try:
#             customer_data = validated_data.pop('customer')
#             customer_instance, _ = Customer.objects.get_or_create(**customer_data)

#             applications_data = validated_data.pop('application')
#             application_details_instance = ApplicationDetails.objects.create(customer=customer_instance, **validated_data)

#             # Add the applications to the ManyToManyField
#             for application_data in applications_data:
#                 application_instance, _ = Application.objects.get_or_create(**application_data)
#                 application_details_instance.application.add(application_instance)

#             print(application_details_instance)
#             return application_details_instance

#         except Exception as e:
#             print("Error:", str(e))
#             return str(e)




# class ApplicationDetailsSerializer(serializers.ModelSerializer):
#     customer = CustomerSerializer()
#     application = ApplicationSerializer(many=True)
#     class Meta:
#         model = ApplicationDetails
#         fields = '__all__'

#     def create(self, validated_data): 
#         try:
#             customer = validated_data.pop('customer')
#             customer_instance, _ = Customer.objects.get_or_create(**customer)
#             application_objs = validated_data.pop('applications')            
#             application_deatils = ApplicationDetails.objects.create(customer=customer_instance, **validated_data)        
#             # Add the applications to the ManyToManyField
#             for application_obj in application_objs:
#                 application_instance, _ = Application.objects.get_or_create(**application_obj)
#                 application_deatils.application.add(application_instance)  
#             print(application_deatils)           
#             return application_deatils
#         except Exception as e:
#             print("Error : ", str(e))
#             return str(e)