from repository import models

class Memory(object):

    def __init__(self, server_obj, info):
        self.server_obj = server_obj
        self.mem_dict = info

    def process(self):
        #内存 数据更新
        pass