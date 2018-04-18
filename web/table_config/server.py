search_config = [
    {'name': 'hostname__contains', 'title': '主机名', 'type': 'input'},
    {'name': 'cabinet_num', 'title': '机柜号', 'type': 'input'},
    {'name': 'server_status_id', 'title': '服务器状态', 'type': 'select', 'choice_name': 'status_choices'},
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
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@id'}},
        'attr': {}
    },
    {
        'q': 'hostname',
        'title': '主机名',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@hostname', }},
        'attr': {'edit-enable': True, 'edit-type': 'input', 'origin': '@hostname','name':'hostname'}
    },
    {
        'q': 'sn',
        'title': 'SN号',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@sn'}},
        'attr': {'edit-enable': True, 'edit-type': 'input', 'origin': '@sn','name':'sn'}
    },
    {
        'q': 'os_platform',
        'title': '系统',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@os_platform'}},
        'attr': {}
    },
    {
        'q': 'os_version',
        'title': '系统版本',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@os_version'}},
        'attr': {}
    },
    {
        'q': 'business_unit__name',
        'title': '业务线',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@business_unit__name'}},
        'attr': {}
    },
    {
        'q': 'server_status_id',
        'title': '服务器状态',
        'display': True,
        'text': {'tpl': '{k1}', 'kwargs': {'k1': '@@status_choices'}},
        'attr': {'edit-enable': True, 'edit-type': 'select', 'choice-key': 'status_choices',
                 'origin': '@server_status_id', 'name':'server_status_id'}
    },
    {
        'q': None,
        'title': '操作',
        'display': True,
        'text': {'tpl': '<a href="/edit/{nid}/">编辑</a> | <a href="/del/{nid}/">删除</a>',
                 'kwargs': {'nid': '@id'}},
    },
]