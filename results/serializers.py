from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from results.models import Result


class ResultSerializer(ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
