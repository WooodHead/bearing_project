#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quotation_item.py
@time: 2018-03-16 10:00
"""

from __future__ import unicode_literals

from flask import (
    request,
    flash,
    render_template,
    abort,
    Blueprint,
)
from flask_babel import gettext as _
from flask_login import login_required
from sqlalchemy import or_

from app_backend import (
    app,
    excel,
)
from app_backend.api.quotation_items import get_quotation_items_rows, get_quotation_items_pagination
from app_backend.forms.quotation_items import QuotationItemsSearchForm
from app_backend.models.model_bearing import QuotationItems
from app_backend.permissions.quotation import (
    permission_quotation_section_search,
    permission_quotation_section_export,
)
from app_common.maps.operations import OPERATION_EXPORT
from app_common.maps.status_delete import (
    STATUS_DEL_NO)

# 定义蓝图
bp_quotation_items = Blueprint('quotation_items', __name__, url_prefix='/quotation/items')

# 加载配置
DOCUMENT_INFO = app.config.get('DOCUMENT_INFO', {})
PER_PAGE_BACKEND = app.config.get('PER_PAGE_BACKEND', 20)
AJAX_SUCCESS_MSG = app.config.get('AJAX_SUCCESS_MSG', {'result': True})
AJAX_FAILURE_MSG = app.config.get('AJAX_FAILURE_MSG', {'result': False})


@bp_quotation_items.route('/lists.html', methods=['GET', 'POST'])
@login_required
@permission_quotation_section_search.require(http_exception=403)
def lists():
    """
    报价列表
    :return:
    """
    template_name = 'quotation/items/lists.html'
    # 文档信息
    document_info = DOCUMENT_INFO.copy()
    document_info['TITLE'] = _('quotation item lists')

    # 搜索条件
    form = QuotationItemsSearchForm(request.form)
    # form.uid.choices = get_quotation_user_list_choices()
    # app.logger.info('')

    search_condition = [
        QuotationItems.status_delete == STATUS_DEL_NO,
    ]
    if request.method == 'POST':
        # 表单校验失败
        if not form.validate_on_submit():
            flash(_('Search Failure'), 'danger')
            # 单独处理csrf_token
            if hasattr(form, 'csrf_token') and getattr(form, 'csrf_token').errors:
                map(lambda x: flash(x, 'danger'), form.csrf_token.errors)
        else:
            if form.customer_cid.data and form.customer_company_name.data:
                search_condition.append(QuotationItems.customer_cid == form.customer_cid.data)
            if form.production_model.data:
                # 注意查询效率
                search_condition.append(
                    or_(
                        QuotationItems.production_model.like('%%%s%%' % form.production_model.data),
                        QuotationItems.enquiry_production_model.like('%%%s%%' % form.production_model.data)
                    )
                )
            if form.start_create_time.data:
                search_condition.append(QuotationItems.create_time >= form.start_create_time.data)
            if form.end_create_time.data:
                search_condition.append(QuotationItems.create_time <= form.end_create_time.data)
        # 处理导出
        if form.op.data == OPERATION_EXPORT:
            # 检查导出权限
            if not permission_quotation_section_export.can():
                abort(403)
            column_names = QuotationItems.__table__.columns.keys()
            query_sets = get_quotation_items_rows(*search_condition)

            return excel.make_response_from_query_sets(
                query_sets=query_sets,
                column_names=column_names,
                file_type='csv',
                file_name='%s.csv' % _('quotation item lists')
            )
    # 翻页数据
    pagination = get_quotation_items_pagination(form.page.data, PER_PAGE_BACKEND, *search_condition)

    # 渲染模板
    return render_template(
        template_name,
        form=form,
        pagination=pagination,
        **document_info
    )
