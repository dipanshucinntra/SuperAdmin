from rest_framework import serializers

from Users.serializers import UserSerializer


from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
