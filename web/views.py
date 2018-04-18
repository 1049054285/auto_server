import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from repository import models
from .service.server import ServerService
from .service.disk import DiskService

def server(request):
    # for i in range(100):
    #     models.Server.objects.create(server_status_id=1,hostname=uuid.uuid1(),sn=uuid.uuid1())
    return render(request, 'server.html')


def add_server_status(server_list):
    """模板语言显示choice"""
    for row in server_list:
        for item in models.Server.server_status_choices:
            if row['server_status_id'] == item[0]:
                row['server_status'] = item[1]
        yield row


class Server_json(View):
    def get(self, request):
        service_obj = ServerService(request)
        return JsonResponse(service_obj.fetch())

    def delete(self, request):
        service_obj = ServerService(request)
        return JsonResponse(service_obj.delete())

    def put(self, request):
        service_obj = ServerService(request)
        return JsonResponse(service_obj.save())

def disk(request):
    return render(request, 'disk.html')

class Disk_json(View):
    def get(self, request):
        service_obj = DiskService(request)
        return JsonResponse(service_obj.fetch())

    def delete(self, request):
        service_obj = DiskService(request)
        return JsonResponse(service_obj.delete())

    def put(self, request):
        service_obj = DiskService(request)
        return JsonResponse(service_obj.save())