import datetime
from repository import models

class Server(object):

    def __init__(self, server_obj, basic_dict, board_dict):
        self.server_obj = server_obj
        self.basic_dict = basic_dict
        self.board_dict = board_dict

    def process(self):
        ret = {'status':True, 'msg':None}
        #服务器 数据更新
        tmp = {}
        tmp.update(self.basic_dict['data'])
        tmp.update(self.board_dict['data'])
        tmp.pop('hostname')
        record_list = []
        from django.db import transaction
        try:
            #事务
            with transaction.atomic():
                for k, new_val in tmp.items():
                    old_val = getattr(self.server_obj, k)
                    if str(old_val) != new_val:
                        setattr(self.server_obj, k, new_val)
                        record = '服务器[%s]的[%s]由[%s]变更为[%s]'%(self.server_obj.hostname,k,old_val,new_val)
                        record_list.append(record)
                self.server_obj.latest_date = datetime.datetime.now()
                self.server_obj.save()
                if record_list:
                    models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(record_list))
        except Exception as e:
            ret['status'] = False
            ret['msg'] = '插件[server]执行出错：%s'%e
        return ret