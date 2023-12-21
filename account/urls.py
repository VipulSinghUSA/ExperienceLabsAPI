from django.urls import path
from .views import UserRegistrationAPIView,ClientExplabsAPIView,LocationAPIView,ClientPkgAPIView,LoginAPIView,CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('clientexplab/', ClientExplabsAPIView.as_view(), name='client_explabs'),
    path('location/', LocationAPIView.as_view(), name='client_explabs'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('client-packages/<str:client_id>/', ClientPkgAPIView.as_view(), name='client-packages'),    
]
