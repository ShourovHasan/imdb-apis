from django.contrib.auth.models import User
from rest_framework import serializers
from user_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    address = serializers.CharField()
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'address', 'gender']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        user.set_password(password)
        user.save()
       
        user_profile = UserProfile(
            user=user,
            address=self.validated_data['address'],
            gender=self.validated_data['gender'],
            role='staff'
        )
        user_profile.save()
        return user