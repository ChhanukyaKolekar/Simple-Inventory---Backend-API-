from rest_framework import serializers
from .models import Items
from django.contrib.auth.models import User

class ItemsSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Items
        fields='__all__'

class RegistrationSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=50)
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already Exist")
        return data

    def create(self,data):
        user = User.objects.create(username=data['name'],email=data['email'])

        user.set_password(data['password'])
        user.save()
        return user
    
class LoginSeriliser(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
