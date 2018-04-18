from django.urls import path
from . import views

urlpatterns = [
    path('server', views.server),
]