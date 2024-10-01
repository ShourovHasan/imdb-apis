from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Subscriber
from .serializers import SubscriberSerializer

class SubscriberCreateView(generics.CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscriber = serializer.save()

        token, created = Token.objects.get_or_create(user=subscriber.user)

        return Response({
            'token': token.key,
            'username': subscriber.user.username,
            'email': subscriber.user.email,
            'address': subscriber.address,
            'gender': subscriber.gender,
        })
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        address = request.data.get('address', 'Unknown Address')
        gender = request.data.get('gender', 'male')

        user = User.objects.create_user(username=username, email=email, password=password)

        subscriber = Subscriber.objects.create(user=user, address=address, gender=gender)

        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            'username': user.username,
            'email': user.email,
            'address': subscriber.address,
            'gender': subscriber.gender,
            'token': token.key,
        }

        return Response(response_data, status=201)