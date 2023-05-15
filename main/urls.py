from django.urls import path
from .views import *

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html'))
    path('create/', CreateCustomUserView.as_view()),
    path('token/', CreateTokenView.as_view()),
    path('user/', RetrieveUpdateUserView.as_view()),
]
