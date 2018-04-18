import json
import importlib
from django.conf import settings
from repository import models
from .server import Server

class PluginManager(object):
    def __init__(self):
        self.plugin_items = settings.PLUGIN_ITEMS
        self.basic_key = 'basic'
        self.board_key = 'board'

    def exec(self, server_dict):
        ret = {'status':True, 'msg':None}
        #检查server表中是否有当前资产信息
        hostname = server_dict['basic']['data']['hostname']
        server_obj = models.Server.objects.filter(hostname=hostname).first()

        #创建 服务器/网卡/内存/硬盘信表记录(这里不创建，需要手动录入服务器信息)
        if not server_obj:
            ret['status'] = False
            ret['msg'] = '该服务器不存在'
            return ret

        #更新 服务器/网卡/内存/硬盘表
        #创建server插件  对象,并执行process方法  更新服务器数据
        server_plugin_obj = Server(server_obj, server_dict[self.basic_key], server_dict[self.board_key])
        result = server_plugin_obj.process()
        if not result['status']:
            ret['status'] = False
            ret['msg'] = result['msg']
        #创建网卡/内存/硬盘插件  对象,并执行process方法  更新 网卡/内存/硬盘数据
        for k, v in self.plugin_items.items():
            try:
                module_path, cls_name = v.rsplit('.',maxsplit=1)
                md = importlib.import_module(module_path)
                cls = getattr(md, cls_name)
                plugin_obj = cls(server_obj, server_dict[k])
                plugin_obj.process()
            except Exception as e:
                ret['status'] = False
                ret['msg'] = '插件[%s]执行出错：%s'%(k,e)
        return ret