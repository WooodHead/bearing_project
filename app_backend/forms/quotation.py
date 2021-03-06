#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: quotation.py
@time: 2018-04-05 22:37
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, IntegerField, SelectField, \
    DecimalField
from wtforms.fields import FieldList, FormField
from wtforms.validators import InputRequired, DataRequired, ValidationError, \
    Optional

from app_common.maps.default import DEFAULT_SEARCH_CHOICES_INT_OPTION




class AmountQuotationValidate(object):
    """
    报价总金额校验（总金额小于1亿）
    报价数量 1-10000
    报价单价 0.00-1000000.00
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        amount_quotation = 0

        for quotation_item in form.quotation_items.entries:
            amount_quotation += (quotation_item.form.quantity.data or 0) * (quotation_item.form.unit_price.data or 0)

        if amount_quotation >= 100000000:
            # raise ValidationError(self.message or _('Data limit exceeded'))
            # TODO why? 使用翻译报错 unicode l'' 这是什么类型
            raise ValidationError(self.message or '数据超出限制')


class QuotationSearchForm(FlaskForm):
    uid = SelectField(
        _('quotation user'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=DEFAULT_SEARCH_CHOICES_INT_OPTION,
        coerce=int,
        description=_('quotation user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('quotation user'),
        }
    )
    customer_cid = IntegerField(
        _('customer company id'),
        validators=[
            InputRequired(),
        ],
        default=0,
        description=_('customer company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company id'),
            'placeholder': _('customer company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    customer_company_name = StringField(
        _('customer company name'),
        validators=[],
        description=_('customer company name'),
        render_kw={
            'placeholder': _('customer company name'),
            'rel': 'tooltip',
            'title': _('customer company name'),
        }
    )

    start_create_time = DateField(
        _('start time'),
        validators=[Optional()],
        description=_('start time'),
        render_kw={
            'placeholder': _('start time'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('start time'),
        }
    )
    end_create_time = DateField(
        _('end time'),
        validators=[Optional()],
        description=_('end time'),
        render_kw={
            'placeholder': _('end time'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('end time'),
        }
    )
    op = IntegerField(
        _('operation'),
        validators=[],
        default=0,
    )
    page = IntegerField(
        _('page'),
        validators=[],
        default=1,
    )


class QuotationItemAddForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False  # disable csrf
        FlaskForm.__init__(self, *args, **kwargs)

    quotation_id = IntegerField(
        _('quotation id'),
        validators=[
        ],
        render_kw={
            'placeholder': _('quotation id'),
            'rel': "tooltip",
            'title': _('quotation id'),
        }
    )
    enquiry_production_model = StringField(
        _('enquiry production model'),
        validators=[],
        default='',
        description=_('enquiry production model'),
        render_kw={
            'placeholder': _('enquiry production model'),
            'rel': 'tooltip',
            'title': _('enquiry production model'),
            'autocomplete': 'off',
        }
    )
    enquiry_quantity = IntegerField(
        _('enquiry quantity'),
        validators=[],
        default=1,
        description=_('enquiry quantity'),
        render_kw={
            'placeholder': _('enquiry quantity'),
            'rel': 'tooltip',
            'title': _('enquiry quantity'),
            'type': 'number',
            'step': 1,
            'min': 1,
            'max': 10000,
        }
    )
    production_id = IntegerField(
        _('production id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'placeholder': _('production id'),
            'rel': "tooltip",
            'title': _('production id'),
            'readonly': 'readonly',
            'type': 'hidden',
        }
    )
    production_brand = StringField(
        _('production brand'),
        validators=[],
        default='',
        description=_('production brand'),
        render_kw={
            'placeholder': _('production brand'),
            'rel': 'tooltip',
            'title': _('production brand'),
            'readonly': 'readonly',
        }
    )
    production_model = StringField(
        _('production model'),
        validators=[],
        default='',
        description=_('production model'),
        render_kw={
            'placeholder': _('production model'),
            'rel': 'tooltip',
            'title': _('production model'),
            'autocomplete': 'off',
        }
    )
    production_sku = StringField(
        _('production sku'),
        validators=[],
        default='',
        description=_('production sku'),
        render_kw={
            'placeholder': _('production sku'),
            'rel': 'tooltip',
            'title': _('production sku'),
            'readonly': 'readonly',
        }
    )
    quantity = IntegerField(
        _('quantity'),
        validators=[],
        default=1,
        description=_('quantity'),
        render_kw={
            'placeholder': _('quantity'),
            'rel': 'tooltip',
            'title': _('quantity'),
            'type': 'number',
            'step': 1,
            'min': 1,
            'max': 10000,
        }
    )
    unit_price = DecimalField(
        _('unit price'),
        validators=[],
        default=0.00,
        description=_('unit price'),
        render_kw={
            'placeholder': _('unit price'),
            'rel': 'tooltip',
            'title': _('unit price'),
            'type': 'number',
            'step': 0.01,
            'min': 0.00,
            'max': 1000000.00,
        }
    )
    note = StringField(
        _('note'),
        validators=[],
        default='',
        description=_('note'),
        render_kw={
            'placeholder': _('note'),
            'rel': 'tooltip',
            'title': _('note'),
        }
    )
    delivery_time = StringField(
        _('delivery time'),
        validators=[],
        default='',
        description=_('delivery time'),
        render_kw={
            'placeholder': _('delivery time'),
            'rel': 'tooltip',
            'title': _('delivery time'),
        }
    )
    status_ordered = BooleanField(
        _('ordered status'),
        default=False,
        validators=[],
        render_kw={
            'rel': 'tooltip',
            'title': _('ordered status'),
        }
    )


class QuotationItemEditForm(QuotationItemAddForm):
    id = IntegerField(
        _('production id'),
        validators=[
            InputRequired(),
        ],
        default=0,
        render_kw={
            'type': 'hidden',
        }
    )


class QuotationAddForm(FlaskForm):
    uid = SelectField(
        _('quotation user'),
        validators=[
            DataRequired(),
        ],
        coerce=int,
        description=_('quotation user'),
        render_kw={
            'rel': 'tooltip',
            'title': _('quotation user'),
        }
    )
    customer_cid = IntegerField(
        _('customer company id'),
        validators=[
            DataRequired(),
        ],
        default=0,
        description=_('customer company id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer company id'),
            'placeholder': _('customer company id'),
            'autocomplete': 'off',
            'type': 'hidden',
        }
    )
    customer_company_name = StringField(
        _('customer company name'),
        validators=[],
        description=_('customer company name'),
        render_kw={
            'placeholder': _('customer company name'),
            'rel': 'tooltip',
            'title': _('customer company name'),
        }
    )
    customer_contact_id = IntegerField(
        _('customer contact id'),
        validators=[
            DataRequired(),
        ],
        default=0,
        description=_('customer contact id'),
        render_kw={
            'rel': 'tooltip',
            'title': _('customer contact id'),
            'type': 'hidden',
        }
    )
    customer_contact_name = StringField(
        _('customer contact name'),
        validators=[],
        description=_('customer contact name'),
        render_kw={
            'placeholder': _('customer contact name'),
            'rel': 'tooltip',
            'title': _('customer contact name'),
        }
    )
    delivery_way = StringField(
        _('delivery way'),
        validators=[],
        description=_('delivery way'),
        render_kw={
            'placeholder': _('delivery way'),
            'rel': 'tooltip',
            'title': _('delivery way'),
        }
    )
    note = StringField(
        _('quotation note'),
        validators=[],
        description=_('quotation note'),
        render_kw={
            'placeholder': _('quotation note'),
            'rel': 'tooltip',
            'title': _('quotation note'),
        }
    )
    status_order = SelectField(
        _('order status'),
        validators=[
            InputRequired(),
        ],
        coerce=int,
        description=_('order status'),
        render_kw={
            'rel': 'tooltip',
            'title': _('order status'),
        }
    )
    amount_quotation = DecimalField(
        _('amount quotation'),
        validators=[
            AmountQuotationValidate()
        ],
        description=_('amount quotation'),
        render_kw={
            'placeholder': _('amount quotation'),
            'rel': 'tooltip',
            'title': _('amount quotation'),
            'type': 'number',
            'disabled': 'disabled',
        }
    )
    data_line_add = IntegerField(
        '数据行新增',
        validators=[],
    )
    data_line_del = IntegerField(
        '数据行删除',
        validators=[],
    )
    quotation_items = FieldList(
        FormField(QuotationItemAddForm),
        label='报价明细',
        min_entries=1,
        max_entries=12,
    )


class QuotationEditForm(QuotationAddForm):
    quotation_items = FieldList(
        FormField(QuotationItemEditForm),
        label='报价明细',
        min_entries=1,
        max_entries=12,
    )
