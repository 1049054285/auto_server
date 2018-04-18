import json
from repository import models
from utils.page import Pagination
from .base import BaseService
from ..table_config import server as server_conf

class ServerService(BaseService):
    def __init__(self, request):
        super(ServerService, self).__init__(request)
        self.table_config = server_conf.table_config
        self.search_config = server_conf.search_config

    def fetch(self):
        """获取数据列表"""
        current_page = self.request.GET.get('pageNum')
        # 获取需要渲染的字段
        values = self.values()
        # 构造 组合查询的Q条件
        condition = self.condition()
        try:
            total_item_count = models.Server.objects.filter(condition).count()
            page_obj = Pagination(current_page, total_item_count, '/web/server')
            server_list = models.Server.objects.filter(condition).values(*values)[page_obj.start:page_obj.end]
        except Exception as e:
            total_item_count = 0
            page_obj = Pagination(current_page, total_item_count, '/web/server')
            server_list = []

        response = {
            'status': True,
            'data_list': list(server_list),
            'table_config': self.table_config,
            'search_config': self.search_config,
            'global_choices_dict': {
                'status_choices': models.Server.server_status_choices
            },
            'pager_html': page_obj.page_html_js()
        }
        return response

    def delete(self):
        """删除数据"""
        response = {'status':True, 'msg':''}
        id_list = json.loads(self.request.body.decode('utf-8'))
        # models.Server.objects.filter(id__in=id_list).delete()
        for nid in id_list:
            try:
                print('delete: ', nid)
                models.Server.objects.filter(id=nid).delete()
            except Exception as e:
                response['status'] = False
                response['msg'] += 'delete server failed(id=%s)：%s|'%(nid,str(e))
        return response

    def save(self):
        """保存(更新)数据"""
        response = {'status':True, 'msg':''}
        update_items = json.loads(self.request.body.decode('utf-8'))
        for item in update_items:
            nid = item.get('id')
            try:
                print('update: ', item)
                item.pop('id')
                models.Server.objects.filter(id=nid).update(**item)
            except Exception as e:
                response['status'] = False
                response['msg'] += 'update server failed(id=%s)：%s|'%(nid,str(e))
        return response

