(function (jq) {
    var requestUrl = '';
    var currentPage = 1;
    var GLOBAL_CHOICES_DICT = {};

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            }
        }
    });

    function getChoiceNameById(key_name, id) {
        var val = '';
        var status_choices_list = GLOBAL_CHOICES_DICT[key_name];
        $.each(status_choices_list, function (index, status) {
            if (status[0] == id) {
                val = status[1];
            }
        });
        return val;
    }

    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    function init(pageNum) {
        console.log('exec init ' + pageNum);
        $('.loading').removeClass('hide');
        var condition = JSON.stringify(getSearchCondition());
        $.ajax({
            url: requestUrl,
            type: 'GET',
            //traditional: true,
            data: {
                'pageNum': pageNum,
                'condition': condition
            },
            success: function (response) {
                initChoices(response.global_choices_dict);
                initTableHead(response.table_config);
                initTableBody(response.data_list, response.table_config);
                initPagerHtml(response.pager_html);
                initSearchCondition(response.search_config);
                $('.loading').addClass('hide');
                currentPage = pageNum;
            },
            error: function () {
                $('.loading').addClass('hide');
            }
        });
    }

    function getSearchCondition() {
        var result = {};
        $('.search-condition').find(':text,select').each(function () {
            var name = $(this).attr('name');
            var value = $(this).val();
            if (result[name]) {
                result[name].push(value);
            } else {
                result[name] = [value];
            }
        });
        return result;
    }

    function bindSearchConditionEvent() {
        /*更新并生成下拉框或输入框*/
        $('.search-condition').on('click', 'li', function () {
            $(this).parent().siblings('label').text($(this).text());
            $(this).parent().parent().next().remove();
            var name = $(this).find('a').attr('name');
            var type = $(this).find('a').attr('type');
            if (type == 'select') {
                var choice_name = $(this).find('a').attr('choice_name');
                // 生成下拉框
                var tag = document.createElement('select');
                tag.className = "form-control no-radius";
                tag.setAttribute('name', name);
                $.each(GLOBAL_CHOICES_DICT[choice_name], function (i, item) {
                    var op = document.createElement('option');
                    op.innerHTML = item[1];
                    op.setAttribute('value', item[0]);
                    $(tag).append(op);
                })
            } else {
                // <input class="form-control no-radius" placeholder="逗号分割多条件" name="hostnmae">
                var tag = document.createElement('input');
                tag.setAttribute('type', 'text');
                // $(tag).addClass('form-control no-radius')
                tag.className = "form-control no-radius";
                tag.setAttribute('placeholder', '请输入条件');
                tag.setAttribute('name', name);
            }
            $(this).parent().parent().after(tag);
        });
        /*添加搜索条件*/
        $('.search-condition .add-condition').click(function () {
            var $condition = $(this).parent().parent().clone();
            $condition.find('.add-condition').removeClass('add-condition').addClass('del-condition').find('span').attr('class', 'glyphicon glyphicon-minus');
            $('.search-condition').append($condition);
        });
        /*删除搜索条件*/
        $('.search-condition').on('click', '.del-condition', function () {
            $(this).parent().parent().remove();
        });
        /*点击搜索按钮*/
        $('.search-bar').on('click', '#search-btn', function () {
            init(1);
        })
    }

    function bindPaginationEvent() {
        $('.pagination li').on('click', 'a', function () {
            var current_page = $(this).attr('page');
            init(current_page);
        })
    }

    function initDefaultSearchCondition(item) {
        if (!$('.input-group').attr('init')) {
            if (item.type == 'input') {
                var tag = document.createElement('input');
                tag.setAttribute('type', 'text');
                tag.className = "form-control no-radius";
                tag.setAttribute('placeholder', '请输入条件');
                tag.setAttribute('name', item.name);
            } else {
                var tag = document.createElement('select');
                tag.className = "form-control no-radius";
                tag.setAttribute('name', item.name);
                $.each(GLOBAL_CHOICES_DICT[item.choice_name], function (i, item) {
                    var op = document.createElement('option');
                    op.innerHTML = item[1];
                    op.setAttribute('value', item[0]);
                    $(tag).append(op);
                })
            }
            $('.input-group').append(tag);
            $('.input-group').attr('init', 'true');
        }
    }

    function initSearchCondition(search_config) {
        var $ul = $('.search-condition :first').find('ul');
        $ul.empty();
        initDefaultSearchCondition(search_config[0]);
        $.each(search_config, function (i, item) {
            var $li = $('<li>');
            var $a = $('<a>');
            $a.text(item['title']);
            $li.append($a);
            $a.attr('name', item['name']);
            $a.attr('type', item['type']);
            if (item['type'] == 'select') {
                $a.attr('choice_name', item['choice_name']);
            }
            $ul.append($li);
            if (!$ul.siblings('label').text()) {
                $ul.siblings('label').text(item['title']);
            }
        });
    }

    function initPagerHtml(pager_html) {
        $('.pagination').empty();
        $('.pagination').append(pager_html);
        bindPaginationEvent();
    }

    function initChoices(global_choices_dict) {
        GLOBAL_CHOICES_DICT = global_choices_dict;
    }

    function initTableHead(table_config) {
        $('#tHead tr').empty();
        $.each(table_config, function (k, item) {
            if (item.display) {
                $('#tHead tr').append('<th>' + item.title + '</th>');
            }
        });
    }

    function initTableBody(data_list, table_config) {
        $('#tBody').empty();
        $.each(data_list, function (k, row_dict) {
            var $tr = $('<tr>');
            $tr.attr('id', row_dict['id']);
            $.each(table_config, function (k, item) {
                if (item.display) {
                    // 处理td的内容变量
                    var format_dict = {};
                    $.each(item.text.kwargs, function (k, v) {
                        if (v.substring(0, 2) == "@@") {
                            var key_name = v.substring(2, v.length);
                            var status_id = row_dict[item.q];
                            format_dict[k] = getChoiceNameById(key_name, status_id);
                        } else if (v[0] == "@" && v[1] != "@") {
                            var col_name = v.substring(1, v.length);
                            format_dict[k] = row_dict[col_name];
                        } else {
                            format_dict[k] = v;
                        }
                    });
                    var $td = $('<td>');
                    // 处理td的属性
                    $.each(item.attr, function (attr_key, attr_val) {
                        if (attr_val[0] == "@") {
                            var col_name = attr_val.substring(1, attr_val.length);
                            attr_val = row_dict[col_name];
                        }
                        $td.attr(attr_key, attr_val)
                    });
                    $td.html(item.text.tpl.format(format_dict));
                    $tr.append($td);
                }
            });
            $('#tBody').append($tr);
        });
    }

    function tdIntoEditMode($td) {
        var edit_type = $td.attr('edit-type');
        if (edit_type == 'input') {
            var input = $('<input>');
            input.addClass('form-control');
            input.css({'padding': '0'});
            var text = $td.text();
            input.val(text);
            $td.html(input);
        } else if (edit_type == 'select') {
            var select = $('<select>');
            select.addClass('form-control');
            select.css({'min-width': '75px'});
            var text = $td.text();
            var choice_key = $td.attr('choice-key');
            var origin = $td.attr('origin');
            $.each(GLOBAL_CHOICES_DICT[choice_key], function (i, item) {
                var op = document.createElement('option');
                op.innerHTML = item[1];
                op.setAttribute('value', item[0]);
                if (item[0] == origin) {
                    op.setAttribute('selected', 'selected');
                }
                select.append(op);
            });
            $td.html(select);
        }
    }

    function tdOutEditMode($td) {
        var editStatus = false;
        var origin = $td.attr('origin');
        if ($td.attr('edit-type') == 'input') {
            var val = $td.find('input').val();
            $td.html(val);
        } else if ($td.attr('edit-type') == 'select') {
            var val = $td.find('select').val();
            var text = $td.find('select')[0].selectedOptions[0].innerText;
            $td.html(text);
            $td.attr('new-value', val);
        }
        if (origin != val) {
            editStatus = true;
        }
        return editStatus;
    }

    function trIntoEditMode($tr) {
        $tr.addClass('success');
        $tr.find('td[edit-enable="true"]').each(function () {
            tdIntoEditMode($(this));
        });
    }

    function trOutEditMode($tr) {
        $tr.removeClass('success');
        $tr.find('td[edit-enable="true"]').each(function () {
            var editStatus = tdOutEditMode($(this));
            if (editStatus) {
                $tr.attr('edit-status', 'true');
            }
        });
    }

    /*单个checkbox进出编辑模式事件*/
    function bindEditModeEvent() {
        $('#tBody').on('click', ':checkbox', function () {
            if ($('#editModeButton').hasClass('btn-warning')) {
                var $tr = $(this).parent().parent();
                if ($(this).prop('checked')) {
                    /*进入编辑模式*/
                    trIntoEditMode($tr);
                } else {
                    /*退出编辑模式*/
                    trOutEditMode($tr);
                }
            }
        })
    }

    /*进入编辑模式*/
    function intoEditMode(){
        $('#editModeButton').addClass('btn-warning').text('退出编辑模式');
        $('#tBody :checked').each(function () {
            var $tr = $(this).parent().parent();
            trIntoEditMode($tr);
        });
    }
    /*退出编辑模式*/
    function outEditMode(){
        $('#editModeButton').removeClass('btn-warning').text('进入编辑模式');
        $('#tBody :checked').each(function () {
            var $tr = $(this).parent().parent();
            trOutEditMode($tr);
        });
    }

    /*按钮组绑定事件*/
    function bindBtnGroupEvent() {
        // 进入和退出编辑模式
        $('#editModeButton').click(function () {
            if ($(this).hasClass('btn-warning')) {
                // 退出编辑模式
                outEditMode();
            } else {
                //进入编辑模式
                intoEditMode();
            }
        });
        // 全选
        $('#chooseAll').click(function () {
            $('#tBody :checkbox').each(function () {
                if (!$(this).prop('checked')) {
                    // 选中
                    $(this).prop('checked', 'checked');
                    // 进入编辑模式
                    if ($('#editModeButton').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        trIntoEditMode($tr);
                    }
                }
            });
        });
        // 取消
        $('#cancelAll').click(function () {
            $('#tBody :checked').each(function () {
                // 选中
                $(this).prop('checked', false);
                // 退出编辑模式
                if ($('#editModeButton').hasClass('btn-warning')) {
                    var $tr = $(this).parent().parent();
                    trOutEditMode($tr);
                }
            });
        });
        // 反选
        $('#reverseAll').click(function () {
            $('#tBody :checkbox').each(function () {
                if (!$(this).prop('checked')) {
                    // 选中
                    $(this).prop('checked', 'checked');
                    // 进入编辑模式
                    if ($('#editModeButton').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        trIntoEditMode($tr);
                    }
                } else {
                    // 取消选中
                    $(this).prop('checked', false);
                    // 退出编辑模式
                    if ($('#editModeButton').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        trOutEditMode($tr);
                    }
                }
            });
        });
        // 删除
        $('#delMulti').click(function () {
            // 弹出模态对话框
            // 给确定按钮绑定事件

        });
        // 给删除模态框的确定按钮绑定事件
        $('#delConfirm-btn').click(function () {
            var ids = [];
            $('#tBody :checked').each(function () {
                ids.push($(this).val());
            });
            $.ajax({
                url: requestUrl,
                type: 'delete',
                data: JSON.stringify(ids),
                traditional: true,
                dataType: 'JSON',
                success: function (data) {
                    if (data.status) {
                        init(currentPage);
                        setTimeout(function () {
                            $('.msg').empty();
                        }, 5000);
                    } else {
                        $('.msg').text(data.msg);
                    }
                }
            });
            $('.modal').modal('hide');

        });
        // 给删除模态框的取消按钮绑定事件
        $('#delCancel-btn').click(function () {
            $('.modal').modal('hide');
        });
        // 保存
        $('#saveMulti').click(function () {
            //先退出编辑模式
            if ($('#editModeButton').hasClass('btn-warning'))
                outEditMode();
            //再执行保存操作
            var update_items = [];
            $('#tBody tr[edit-status="true"]').each(function () {
                var temp = {};
                var id = $(this).attr('id');
                temp['id'] = id;
                $(this).children('td[edit-enable="true"]').each(function () {
                    var origin = $(this).attr('origin');
                    var name = $(this).attr('name');
                    if ($(this).attr('edit-type') == 'select') {
                        var newValue = $(this).attr('new-value');
                    } else {
                        var newValue = $(this).text();
                    }
                    if(newValue != origin) {
                        temp[name] = newValue;
                    }
                });

                update_items.push(temp);
            });
            console.log(update_items);
            //向后台发送数据 PUT
            $.ajax({
                url: requestUrl,
                type: 'put',
                data: JSON.stringify(update_items),
                traditional: true,
                dataType: 'JSON',
                success: function (data) {
                    if (data.status) {
                        $('.msg').text('保存成功');
                        setTimeout(function () {
                            $('.msg').empty();
                        }, 5000);
                    } else {
                        $('.msg').text(data.msg);
                    }
                }
            });
        });
    }

    ctrlKeyStatus = false;
    window.onkeydown = function (event) {
        if(event && event.keyCode == 17){
            ctrlKeyStatus = true;
        }
    };
    window.onkeyup = function (event) {
        if(event && event.keyCode == 17){
            ctrlKeyStatus = false;
        }
    };

    /*给表格中的下拉框绑定change事件*/
    function bindSelectChangeEvent(){
        $('#tBody').on('change', 'select', function () {
            if(ctrlKeyStatus){
                var v = $(this).val();
                var $tr = $(this).parent().parent();
                $tr.nextAll().each(function () {
                    if($(this).find(':checkbox').prop('checked')){
                        $(this).find('select').val(v);
                    }
                });
            }
        })
    }

    jq.extend({
        'table_list': function (url) {
            requestUrl = url;
            init(1);
            bindSearchConditionEvent();
            bindEditModeEvent();
            bindBtnGroupEvent();
            bindSelectChangeEvent();
        }
    });
})
(jQuery);
