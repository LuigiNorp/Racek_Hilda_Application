from django.urls import path
from .views import *

urlpatterns = [
    path('usuario', UsuarioAPIView.as_view(), name='usuario'),
]
