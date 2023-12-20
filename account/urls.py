from django.urls import path
from .views import UserRegistrationAPIView,ClientExplabsAPIView,LocationAPIView,ClientPkgAPIView,UserLoginAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('clientexplab/', ClientExplabsAPIView.as_view(), name='client_explabs'),
    path('location/', LocationAPIView.as_view(), name='client_explabs'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('client-packages/<str:client_id>/', ClientPkgAPIView.as_view(), name='client-packages'),    
]
