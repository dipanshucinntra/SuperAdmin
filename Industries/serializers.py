from rest_framework import serializers
from .models import *


class IndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        fields = '__all__'