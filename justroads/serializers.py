from rest_framework import serializers
from rest_framework.authtoken.models import Token

from justroads.models import (
    Defect,
    DefectStatus,
    Mark,
    MarkAnnotation,
)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class LogoutSerializer(serializers.Serializer):
    pass


class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defect
        fields = '__all__'


class DefectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectStatus
        fields = '__all__'


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'


class MarkAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkAnnotation
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
