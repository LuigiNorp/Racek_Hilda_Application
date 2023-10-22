from django.urls import include, path
from .views import CreateCustomUserView, CreateTokenView, PersonalViewset, ClienteViewset, CurpViewset, RetrieveUpdateUserView, EditProfileView
from .models import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'personal', PersonalViewset, basename='personal')
router.register(r'client', ClienteViewset, basename='client')
router.register(r'curp', CurpViewset, basename='curp')

urlpatterns = [
    path('create/', CreateCustomUserView.as_view(), name='create_user'),
    path('token/', CreateTokenView.as_view(), name='create_token'),
    path('user/', RetrieveUpdateUserView.as_view(), name='retrieve_update_user'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('', include(router.urls)),
]
    
