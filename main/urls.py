from django.urls import path
from .views import *

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html'))
    path('', HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view() , name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('forget-password/', ForgetPasswordView.as_view() , name="forget_password"),
    path('change-password/<token>/', ChangePasswordView.as_view() , name="change_password"),
    path('logout/' , LogoutView.as_view() , name="logout"),
    path('users/', UsersView.as_view(), name='users'),
    path('user/<int:pk>/profile/', CustomUserProfileView.as_view(), name="profile"),
    path('clients/', ClientesView.as_view(), name="clients"),
    path('previous/', PersonalView.as_view(), name="previous"),
    path('employees/', PersonalView.as_view(), name="employees"),
    path('user/<int:pk>/history/', UserHistoryView.as_view(), name="history"),
]
