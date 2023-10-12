from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username is Taken")
        
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("email is Taken")
            
        return data
    
    def create(self,validated_data):
        user = User.objects.create_user(username = validated_data['username'],email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['stream']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        depth = 1
        
    # stream = StreamSerializer()

    def validate(self,data):
        self.special_char = "<>/,!@#$%^&*|=+_-"
        if any(c in self.special_char for c in data['name']):
            raise serializers.ValidationError("No Special Characters are Allowed")
        

        if data['age'] < 18:
            raise serializers.ValidationError("Age should be 18+ ")
        
        return data