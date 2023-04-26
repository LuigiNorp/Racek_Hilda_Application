from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id','username','email', 'password','nombre','apellido_paterno','apellido_materno','departamento')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password',None)
        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        
        return user

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(style={'input:type':'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password=password
        )

        if not user:
            raise serializers.ValidationError('No se pudo realizar la autenticación satisfactoriamente', code='authorization')
        
        data['user'] = user
        return data