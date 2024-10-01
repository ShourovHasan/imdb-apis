from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Subscriber

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class SubscriberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Subscriber
        fields = ['username', 'email', 'password', 'address', 'gender']

    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('user')['username'],
            'email': validated_data.pop('user')['email'],
            'password': validated_data.pop('password')
        }
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        subscriber = Subscriber(user=user, **validated_data)
        subscriber.save()
        return subscriber
