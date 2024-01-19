from rest_framework import serializers
from .models import *

class ApplicationSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Application
        fields = '__all__'

      