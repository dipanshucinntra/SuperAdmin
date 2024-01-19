from Applications.serializers import ApplicationSerializer
from Industries.serializers import IndustriesSerializer
from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    industry = IndustriesSerializer(many=True, read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'

class ApplicationDetailsSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=True, read_only=True)
    application = ApplicationSerializer(many=True, read_only=True)
    class Meta:
        model = ApplicationDetails
        fields = '__all__'
