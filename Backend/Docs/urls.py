
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PDF, name='PDF'),
]
