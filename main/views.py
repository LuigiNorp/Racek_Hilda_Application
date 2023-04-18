from django.shortcuts import redirect, render
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login
from main.forms import signupform
from .serializers import UserSerializer, AuthTokenSerializer
from .models import Usuario

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    model_class = Usuario

class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    model_class = Usuario
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


# class UsuarioAPIView(APIView):
#     def get(self, _):
#         usuarios = Usuario.objects.all()
#         usuario = random.choice(usuarios)
#         return Response({
#             'id':usuario.id
#             })

# def index(request):
#     return render(request, 'index.html')


def SignupView(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = signupform()
    return render(request, 'signup.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    else:
        return render(request, 'login.html')

def Index(request):
    return render(request, 'index.html')

