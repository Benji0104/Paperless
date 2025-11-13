
from django.urls import path
from .Views import views_Docs

urlpatterns = [
    path('', views_Docs.PDF, name='PDF'),
]
