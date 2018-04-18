import json


class BaseService(object):
    def __init__(self, request):
    #     self.table_config = server_conf.table_config
    #     self.search_config = server_conf.search_config
        self.request = request

    def values(self):
        values = []
        for item in self.table_config:
            if item['q']:
                values.append(item['q'])
        return values

    def condition(self):
        # 获取搜索条件
        condition_dict = json.loads(self.request.GET.get('condition'))
        from django.db.models import Q
        condition = Q()
        if condition_dict:
            for k, v in condition_dict.items():
                temp = Q()
                temp.connector = 'OR'
                for item in v:
                    temp.children.append((k, item))
                condition.add(temp, 'AND')
        return condition