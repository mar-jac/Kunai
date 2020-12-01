from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import Student


class StudentSerializer(ModelSerializer):
    first_name = serializers.CharField(read_only=True, source="user.first_name")
    last_name = serializers.CharField(read_only=True, source="user.last_name")

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name')
