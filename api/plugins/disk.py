import json
from repository import models

class Disk(object):
    def __init__(self, server_obj, info):
        self.server_obj = server_obj
        self.disk_dict = info

    def process(self):
        #硬盘 数据更新
        new_disk_info_dict = self.disk_dict['data']
        old_disk_list = self.server_obj.disk.all()
        new_disk_slot_set = set(new_disk_info_dict.keys())
        old_disk_slot_set = {obj.slot for obj in old_disk_list}
        del_slot_list = old_disk_slot_set.difference(new_disk_slot_set)
        add_slot_list = new_disk_slot_set.difference(old_disk_slot_set)
        update_slot_list = new_disk_slot_set.intersection(old_disk_slot_set)
        #新增的槽位
        self.add_disk(add_slot_list, new_disk_info_dict)
        #删除的槽位
        self.del_disk(del_slot_list)
        #待确认是否需要更新的槽位
        self.update_disk(update_slot_list,new_disk_info_dict)


    def add_disk(self, add_slot_list, new_disk_info_dict):
        add_record_list = []
        for slot in add_slot_list:
            value = new_disk_info_dict[slot]
            record = '服务器[%s]的槽位[%s]上添加硬盘：[%s]'%(self.server_obj.hostname,slot,json.dumps(value))
            add_record_list.append(record)
            value['server_obj'] = self.server_obj
            models.Disk.objects.create(**value)
        if add_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(add_record_list))

    def del_disk(self,del_slot_list):
        del_record_list = []
        for slot in del_slot_list:
            old_disk_info_dict = models.Disk.objects.filter(server_obj=self.server_obj,slot=slot).values('slot','model','capacity','pd_type').first()
            record = '服务器[%s]的槽位[%s]上的硬盘[%s]被移除'%(self.server_obj.hostname,slot,json.dumps(old_disk_info_dict))
            del_record_list.append(record)
        if del_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(del_record_list))
        models.Disk.objects.filter(server_obj=self.server_obj, slot__in=del_slot_list).delete()

    def update_disk(self,update_slot_list,new_disk_info_dict):
        update_record_list = []
        for slot in update_slot_list:
            flag = False
            value = new_disk_info_dict[slot]
            obj = models.Disk.objects.filter(server_obj=self.server_obj,slot=slot).first()
            for k,new_val in value.items():
                old_val = getattr(obj, k)
                if str(old_val) != new_val:
                    setattr(obj, k, new_val)
                    flag = True
            if flag:
                old_disk_info_dict = models.Disk.objects.filter(server_obj=self.server_obj,slot=slot).values('slot','model','capacity','pd_type').first()
                record = '服务器[%s]的槽位[%s]上的硬盘由[%s]更换为[%s]'%(self.server_obj.hostname,slot,json.dumps(old_disk_info_dict),json.dumps(value))
                update_record_list.append(record)
                obj.save()
        if update_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(update_record_list))