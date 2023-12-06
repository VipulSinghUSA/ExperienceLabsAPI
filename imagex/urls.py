from django.urls import path

from .views import UserLoginAPIView, ClientPkgAPIView, AccountAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('client-packages/<str:client_id>/', ClientPkgAPIView.as_view(), name='client-packages'),
    path('account/<str:client_id>/', AccountAPIView.as_view(), name='client-packages'),

]
