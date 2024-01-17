from rest_framework import serializers
from .models import *


class PyamentsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PyamentsHistory
        fields = "__all__"


class AttachmentSerializer(serializers.ModelSerializer):
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
