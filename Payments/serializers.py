from rest_framework import serializers
from Customers.models import Customer
from .models import *


class PyamentsHistorySerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  
    class Meta:
        model = PyamentsHistory
        fields = "__all__"


class AttachmentSerializer(serializers.ModelSerializer):
    payment = serializers.PrimaryKeyRelatedField(queryset=PyamentsHistory.objects.all()) 
    class Meta:
        model = Attachment
        fields = "__all__"


class AttachPyamentsSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField('get_attachments')
    class Meta:
        model = PyamentsHistory
        fields = "__all__"

    def get_attachments(self, obj):
        if Attachment.objects.filter(link_id=obj.id).exists():
            objs = Attachment.objects.filter(link_id=obj.id)
            serializer = AttachmentSerializer(objs, many=True)
            return serializer.data
        else:
            return ""
