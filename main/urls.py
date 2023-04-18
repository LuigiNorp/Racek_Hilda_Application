from django.urls import path
from .views import *
from django.views.generic import TemplateView


urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html'))
    path('create/', CreateUserView.as_view()),
    path('token/', CreateTokenView.as_view()),
    path('user/', RetrieveUpdateUserView.as_view()),
]
