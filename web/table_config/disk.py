search_config = [
    {'name': 'model__contains', 'title': '型号', 'type': 'input'},
    {'name': 'capacity', 'title': '磁盘容量GB', 'type': 'input'},
]
table_config = [
    {
        'q': None,
        'title': '选择',
        'display': True,
        'text': {'tpl': '<input type="checkbox" value="{k1}" />', 'kwargs': {'k1': '@id'}},
        'attr': {'nid': '@id'}
    },
    {
        'q': 'id',
        'title': 'ID',
        'display': False,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@id'}},
        'attr': {}
    },
    {
        'q': 'slot',
        'title': '插槽位',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@slot'}},
        'attr': {}
    },
    {
        'q': 'model',
        'title': '磁盘型号',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@model'}},
        'attr': {'edit-enable': True, 'edit-type': 'input', 'origin': '@model','name':'model'}
    },
    {
        'q': 'capacity',
        'title': '磁盘容量GB',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@capacity'}},
        'attr': {'edit-enable': True, 'edit-type': 'input', 'origin': '@capacity','name':'capacity'}
    },
    {
        'q': 'pd_type',
        'title': '磁盘类型',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@pd_type'}},
        'attr': {}
    },
    {
        'q': 'server_obj__hostname',
        'title': '所属服务器',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@server_obj__hostname'}},
        'attr': {}
    },
]