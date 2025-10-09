from django.urls import path
from .Views.login import login

urlpatterns = [
    path('', login, name='login'),
]