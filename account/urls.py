from django.urls import path

from .views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('clientexplab/<str:client_id>/', ClientExplabsAPIView.as_view(), name='client_explabs'),
    path('location/<str:client_id>/', LocationAPIView.as_view(), name='client_explabs'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('countries/', CountryAPIView.as_view(), name='country-list'),
    # path('location/list/', listLocationAPIView.as_view(), name='location-list'),
    path('client-packages/<str:client_id>/', ClientPkgAPIView.as_view(), name='client-packages'), 
    path('user/profile/', UserProfileAPIView.as_view(), name='client-packages'),
    path('list/location/', LocationListAPIView.as_view()),
    path('invoices/', InvoiceCreateView.as_view(), name='invoice-create'),

   
]
