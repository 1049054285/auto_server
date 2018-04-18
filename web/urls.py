from django.urls import path
from . import views

urlpatterns = [
    path('server', views.server),
    path('disk', views.disk),
    path('server_json', views.Server_json.as_view()),
    path('disk_json', views.Disk_json.as_view()),
]