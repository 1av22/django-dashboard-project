from django.urls import path
from .views import DataListAPIView

urlpatterns = [
    path('data/', DataListAPIView.as_view(), name='data_list')
]
