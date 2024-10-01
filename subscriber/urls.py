from django.urls import path
from .views import SubscriberCreateView

urlpatterns = [
    path('register/', SubscriberCreateView.as_view(), name='register'),
]
