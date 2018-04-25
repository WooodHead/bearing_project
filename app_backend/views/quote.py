#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quote.py
@time: 2018-03-16 09:59
"""


from __future__ import unicode_literals

import json
from copy import copy
from datetime import datetime

from flask import (
    request,
    flash,
    render_template,
    url_for,
    redirect,
    abort,
    jsonify,
    Blueprint,
)
from flask_babel import gettext as _
from flask_login import login_required

from app_backend import (
    app,
    excel,
)
from app_backend.api.quote import (
    get_quote_pagination,
    get_quote_row_by_id,
    add_quote,
    edit_quote,
    get_quote_rows,
    quote_total_stats,
    quote_order_stats,
)
from app_backend.api.user import (
    get_user_rows
)
from app_backend.forms.quote import (
    QuoteSearchForm,
    QuoteAddForm,
    QuoteEditForm,
)
from app_backend.models.bearing_project import Quote
from app_backend.permissions import (
    permission_quote_section_add,
    permission_quote_section_search,
    permission_quote_section_export,
    permission_quote_section_stats,
    QuoteItemGetPermission,
    QuoteItemEditPermission,
    QuoteItemDelPermission,
)
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.status_delete import (
    STATUS_DEL_OK,
    STATUS_DEL_NO)
from app_common.maps.type_role import (
    TYPE_ROLE_SALES,
)
from app_common.tools import json_default

# 定义蓝图
bp_quote = Blueprint('quote', __name__, url_prefix='/quote')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


def get_sales_user_list():
    sales_user_list = copy(default_choices_int)
    user_list = get_user_rows(**{'role_id': TYPE_ROLE_SALES})
    sales_user_list.extend([(0, '-')])
    sales_user_list.extend([(user.id, user.name) for user in user_list])
    return sales_user_list


@bp_quote.route('/lists.html', methods=['GET', 'POST'])
@bp_quote.route('/lists/<int:page>.html', methods=['GET', 'POST'])
@login_required
@permission_quote_section_search.require(http_exception=403)
def lists(page=1):
    """
    报价列表
    :param page:
    :return:
    """
    template_name = 'quote/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote lists')

    # 搜索条件
    form = QuoteSearchForm(request.form)
    form.quote_brand.choices = get_sales_user_list()
    # app.logger.info('')

    search_condition = [
        Quote.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.company_name.data:
                search_condition.append(Quote.company_name == form.company_name.data)
            if form.company_type.data != default_choice_option_int:
                search_condition.append(Quote.company_type == form.company_type.data)
            if form.owner_uid.data != default_choice_option_int:
                search_condition.append(Quote.owner_uid == form.owner_uid.data)
            if form.start_create_time.data:
                search_condition.append(Quote.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(Quote.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == 1:
            # 检查导出权限
            if not permission_quote_section_export.can():
                abort(403)
            column_names = Quote.__table__.columns.keys()
            query_sets = get_quote_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('quote lists')
            )
    # 翻页数据
    pagination = get_quote_pagination(page, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )


@bp_quote.route('/<int:quote_id>/info.html')
@login_required
def info(quote_id):
    """
    报价详情
    :param quote_id:
    :return:
    """
    # 检查读取权限
    quote_item_get_permission = QuoteItemGetPermission(quote_id)
    if not quote_item_get_permission.can():
        abort(403)
    # 详情数据
    quote_info = get_quote_row_by_id(quote_id)
    # 检查资源是否存在
    if not quote_info:
        abort(404)
    # 检查资源是否删除
    if quote_info.status_delete == STATUS_DEL_OK:
        abort(410)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote info')
    # 渲染模板
    return render_template('quote/info.html', quote_info=quote_info, **document_info)


@bp_quote.route('/add.html', methods=['GET', 'POST'])
@login_required
@permission_quote_section_add.require(http_exception=403)
def add():
    """
    创建报价
    :return:
    """
    template_name = 'quote/add.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote add')

    # 加载创建表单
    form = QuoteAddForm(request.form)

    # 进入创建页面
    if request.method == 'GET':
        # 渲染页面
        return render_template(
            template_name,
            form=form,
            **document_info
        )

    # 处理创建请求
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )

        # 表单校验成功
        current_time = datetime.utcnow()
        quote_data = {
            'company_name': form.company_name.data,
            'company_address': form.company_address.data,
            'company_site': form.company_site.data,
            'company_tel': form.company_tel.data,
            'company_fax': form.company_fax.data,
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'create_time': current_time,
            'update_time': current_time,
        }
        result = add_quote(quote_data)
        # 创建操作成功
        if result:
            flash(_('Add Success'), 'success')
            return redirect(request.args.get('next') or url_for('quote.lists'))
        # 创建操作失败
        else:
            flash(_('Add Failure'), 'danger')
            return render_template(
                template_name,
                form=form,
                **document_info
            )


@bp_quote.route('/<int:quote_id>/edit.html', methods=['GET', 'POST'])
@login_required
def edit(quote_id):
    """
    报价编辑
    """
    # 检查编辑权限
    quote_item_edit_permission = QuoteItemEditPermission(quote_id)
    if not quote_item_edit_permission.can():
        abort(403)

    quote_info = get_quote_row_by_id(quote_id)
    # 检查资源是否存在
    if not quote_info:
        abort(404)
    # 检查资源是否删除
    if quote_info.status_delete == STATUS_DEL_OK:
        abort(410)

    template_name = 'quote/edit.html'

    # 加载编辑表单
    form = QuoteEditForm(request.form)

    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote edit')

    # 进入编辑页面
    if request.method == 'GET':
        # 表单赋值
        form.company_name.data = quote_info.company_name
        form.company_address.data = quote_info.company_address
        form.company_site.data = quote_info.company_site
        form.company_tel.data = quote_info.company_tel
        form.company_fax.data = quote_info.company_fax
        form.company_type.data = quote_info.company_type
        form.owner_uid.data = quote_info.owner_uid
        form.status_delete.data = quote_info.status_delete
        form.delete_time.data = quote_info.delete_time
        form.create_time.data = quote_info.create_time
        form.update_time.data = quote_info.update_time
        # 渲染页面
        return render_template(
            template_name,
            quote_id=quote_id,
            form=form,
            **document_info
        )

    # 处理编辑请求
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                quote_id=quote_id,
                form=form,
                **document_info
            )
        # 表单校验成功
        current_time = datetime.utcnow()
        quote_data = {
            'company_name': form.company_name.data,
            'company_address': form.company_address.data,
            'company_site': form.company_site.data,
            'company_tel': form.company_tel.data,
            'company_fax': form.company_fax.data,
            'company_type': form.company_type.data,
            'owner_uid': form.owner_uid.data,
            'update_time': current_time,
        }
        result = edit_quote(quote_id, quote_data)
        # 编辑操作成功
        if result:
            flash(_('Edit Success'), 'success')
            return redirect(request.args.get('next') or url_for('quote.lists'))
        # 编辑操作失败
        else:
            flash(_('Edit Failure'), 'danger')
            return render_template(
                template_name,
                quote_id=quote_id,
                form=form,
                **document_info
            )


@bp_quote.route('/ajax/del', methods=['GET', 'POST'])
@login_required
def ajax_delete():
    """
    报价删除
    :return:
    """
    ajax_success_msg = AJAX_SUCCESS_MSG.copy()
    ajax_failure_msg = AJAX_FAILURE_MSG.copy()

    # 检查请求方法
    if not (request.method == 'GET' and request.is_xhr):
        ajax_failure_msg['msg'] = _('Del Failure')  # Method Not Allowed
        return jsonify(ajax_failure_msg)

    # 检查请求参数
    quote_id = request.args.get('quote_id', 0, type=int)
    if not quote_id:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)

    # 检查删除权限
    quote_item_del_permission = QuoteItemDelPermission(quote_id)
    if not quote_item_del_permission.can():
        ajax_failure_msg['msg'] = _('Del Failure')  # Permission Denied
        return jsonify(ajax_failure_msg)

    quote_info = get_quote_row_by_id(quote_id)
    # 检查资源是否存在
    if not quote_info:
        ajax_failure_msg['msg'] = _('Del Failure')  # ID does not exist
        return jsonify(ajax_failure_msg)
    # 检查资源是否删除
    if quote_info.status_delete == STATUS_DEL_OK:
        ajax_success_msg['msg'] = _('Del Success')  # Already deleted
        return jsonify(ajax_success_msg)

    current_time = datetime.utcnow()
    quote_data = {
        'status_delete': STATUS_DEL_OK,
        'delete_time': current_time,
        'update_time': current_time,
    }
    result = edit_quote(quote_id, quote_data)
    if result:
        ajax_success_msg['msg'] = _('Del Success')
        return jsonify(ajax_success_msg)
    else:
        ajax_failure_msg['msg'] = _('Del Failure')
        return jsonify(ajax_failure_msg)


@bp_quote.route('/ajax/stats', methods=['GET', 'POST'])
@login_required
def ajax_stats():
    """
    获取报价统计
    :return:
    """
    time_based = request.args.get('time_based', 'hour')
    result_quote_middleman = quote_middleman_stats(time_based)
    result_quote_end_user = quote_end_user_stats(time_based)

    line_chart_data = {
        'labels': [label for label, _ in result_quote_middleman],
        'datasets': [
            {
                'label': '同行',
                'backgroundColor': 'rgba(220,220,220,0.5)',
                'borderColor': 'rgba(220,220,220,1)',
                'pointBackgroundColor': 'rgba(220,220,220,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_quote_middleman]
            },
            {
                'label': '终端',
                'backgroundColor': 'rgba(151,187,205,0.5)',
                'borderColor': 'rgba(151,187,205,1)',
                'pointBackgroundColor': 'rgba(151,187,205,1)',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
                'data': [data for _, data in result_quote_end_user]
            }
        ]
    }
    return json.dumps(line_chart_data, default=json_default)


@bp_quote.route('/stats.html')
@login_required
@permission_quote_section_stats.require(http_exception=403)
def stats():
    """
    报价统计
    :return:
    """
    # 统计数据
    time_based = request.args.get('time_based', 'hour')
    if time_based not in ['hour', 'date', 'month']:
        abort(404)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote stats')
    # 渲染模板
    return render_template(
        'quote/stats.html',
        time_based=time_based,
        **document_info
    )


@bp_quote.route('/<int:quote_id>/stats.html')
@login_required
@permission_quote_section_stats.require(http_exception=403)
def stats_item(quote_id):
    """
    报价统计明细
    :param quote_id:
    :return:
    """
    quote_info = get_quote_row_by_id(quote_id)
    # 检查资源是否存在
    if not quote_info:
        abort(404)
    # 检查资源是否删除
    if quote_info.status_delete == STATUS_DEL_OK:
        abort(410)

    # 统计数据
    quote_stats_item_info = get_quote_row_by_id(quote_id)
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quote stats item')
    # 渲染模板
    return render_template(
        'quote/stats_item.html',
        quote_stats_item_info=quote_stats_item_info,
        **document_info
    )
