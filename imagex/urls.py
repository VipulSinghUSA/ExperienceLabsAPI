from django.urls import path
from .views import AccountAPIView

urlpatterns = [
    path('account/<str:client_id>/', AccountAPIView.as_view(), name='client-packages'),

]
