from django.urls import path
from .views import *
from .models import *

all_models = [model.__name__ for model in globals().values() if isinstance(model, type) and issubclass(model, models.Model)]

urlpatterns = []

for model in all_models:
    viewset = globals().get(f"{model}ViewSet", None)
    if viewset:
        urlpatterns += [
            path(f"{model.lower()}", viewset.as_view({
                'get': 'list',
                'post': 'create'
            })),
            path(f"{model.lower()}/<str:pk>", viewset.as_view({
                'get': 'retrieve',
                'put': 'update',
                'delete': 'destroy'
            })),
        ]