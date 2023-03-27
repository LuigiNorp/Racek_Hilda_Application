from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Usuario
import random

# Create your views here.
class UsuarioAPIView(APIView):
    def get(self, _):
        usuarios = Usuario.objects.all()
        usuario = random.choice(usuarios)
        return Response({
            'id':usuario.id
            })
