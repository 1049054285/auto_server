from django.urls import path
from . import views

urlpatterns = [
    path('server', views.server),
    path('callback', views.test_callback),
]