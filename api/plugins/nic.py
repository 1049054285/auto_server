from repository import models

class Nic(object):
    
    def __init__(self, server_obj, info):
        self.server_obj = server_obj
        self.nic_dict = info

    def process(self):
        #网卡 数据更新
        pass