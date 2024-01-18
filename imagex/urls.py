from django.urls import path
from .views import AccountAPIView,RecordLocationByClientId,RemoveBackgroundAPIView

urlpatterns = [
    path('account/<str:client_id>/', AccountAPIView.as_view(), name='client-packages'),
    path('records/<str:client_id>/', RecordLocationByClientId.as_view(), name='record-by-client-id'),
    path('remove-background/', RemoveBackgroundAPIView.as_view(), name='remove_background'),

]
