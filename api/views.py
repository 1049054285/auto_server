from django.shortcuts import render, redirect, HttpResponse
from  django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from datetime import date
import hashlib
import time
from .plugins import PluginManager
from repository import models

def md5(arg):
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()

key = "asdfuasodijfoausfnasdf"
# redis,Memcache
visited_keys = {
    # "841770f74ef3b7867d90be37c5b4adfc":时间,  10
}

def api_auth(func):
    def inner(request, *args, **kwargs):
        server_float_ctime = time.time()
        auth_header_val = request.META.get('HTTP_AUTH_API')
        print('auth_header_val:',auth_header_val)
        # 841770f74ef3b7867d90be37c5b4adfc|1506571253.9937866
        if auth_header_val:
            client_md5_str, client_ctime = auth_header_val.split('|', maxsplit=1)
            client_float_ctime = float(client_ctime)
            # 第一关
            if (client_float_ctime + 20) < server_float_ctime:
                return HttpResponse('API token value expires')
            # 第二关：
            server_md5_str = md5("%s|%s" % (key, client_ctime,))
            if server_md5_str != client_md5_str:
                return HttpResponse('API token value is invalid')
            # 第三关：
            if visited_keys.get(client_md5_str):
                return HttpResponse('API token value is invalid')
            visited_keys[client_md5_str] = client_float_ctime
        else:
            return HttpResponse('API token value is invalid')
        return func(request, *args, **kwargs)
    return inner


@csrf_exempt
@api_auth
def server(request):
    """接收处理客户端提交的服务器资产数据"""
    if request.method == 'GET':
        #获取今日未采集服务器
        today_date = date.today()
        hostname_list = models.Server.objects.filter(
            Q(Q(latest_date=None)|Q(latest_date__date__lt=today_date))&Q(server_type_id=2)
        ).values('hostname')[:200]
        hostname_list = list(hostname_list)
        return HttpResponse(json.dumps(hostname_list))

    if request.method == 'POST':
        #客户端提交最新服务器资产数据
        server_dict = json.loads(request.body.decode('utf-8'))
        #检查资产信息状态是否正常
        if not server_dict['basic']['status']:
            return HttpResponse('The basic info status was wrong')
        manager = PluginManager()
        result = manager.exec(server_dict)

        return HttpResponse(json.dumps(result))


@csrf_exempt
def test_callback(request):
    """用于测试第三方回掉接口"""
    print('request.META:', request.META)
    print('request.body:', request.body.decode('utf-8'))
    return HttpResponse(json.dumps({'request.META': request.META, 'request.body': request.body.decode('utf-8')}))
