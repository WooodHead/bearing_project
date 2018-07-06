#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: customer.py
@time: 2018-03-16 14:41
"""

from __future__ import unicode_literals

import time
from datetime import datetime, timedelta
from six import iteritems
from flask_babel import lazy_gettext as _

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress
from app_common.maps.default import default_choices_int, default_choice_option_int
from app_common.maps.type_company import TYPE_COMPANY_DICT

from copy import copy

company_type_choices = copy(default_choices_int)
company_type_choices.extend(iteritems(TYPE_COMPANY_DICT))


class CustomerSearchForm(FlaskForm):
    """
    搜索表单
    """
    company_name = StringField(
        _('company name'),
        validators=[],
        description=_('company name'),
        render_kw={
            'placeholder': _('company name'),
            'rel': 'tooltip',
            'title': _('company name'),
        }
    )
    company_type = SelectField(
        _('company type'),
        validators=[
            InputRequired(),  # 可以为0
        ],
        default=default_choice_option_int,
        coerce=int,
        choices=company_type_choices,
        description=_('company type'),
        render_kw={
            'rel': 'tooltip',
            'title': _('company type'),
        }
    )
    owner_uid = SelectField(
        _('owner uid'),
        default=default_choice_option_int,
        # validators=[],
        coerce=int,
        description=_('owner uid'),
        render_kw={
            'rel': 'tooltip',
            'title': _('owner uid'),
        }
    )
    start_create_time = DateField(
        _('start time'),
        validators=[],
        default=datetime.utcnow() - timedelta(days=30),
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
        validators=[],
        default=datetime.utcnow(),
        description=_('end time'),
        render_kw={
            'placeholder': _('end time'),
            'type': 'date',
            'rel': 'tooltip',
            'title': _('end time'),
        }
    )
    op = IntegerField(
        _('Option'),
        validators=[],
        default=0,
    )


class CustomerAddForm(FlaskForm):
    """
    创建表单（字段一般带有默认选项）
    """
    company_name = StringField(
        _('company name'),
        validators=[DataRequired(), Length(max=100)],
        description='公司名称，最大长度100字符'
    )
    company_address = StringField(
        _('company address'),
        validators=[DataRequired(), Length(max=100)],
        description='公司地址，最大长度100字符'
    )
    company_site = StringField(
        _('company site'),
        validators=[DataRequired(), Length(max=100)],
        description='公司官网，最大长度100字符'
    )
    company_tel = StringField(
        _('company tel'),
        validators=[DataRequired(), Length(max=100)],
        description='公司电话，最大长度100字符'
    )
    company_fax = StringField(
        _('company fax'),
        validators=[DataRequired(), Length(max=100)],
        description='公司传真，最大长度100字符'
    )
    company_type = IntegerField(
        _('company type'),
        validators=[DataRequired()],
        default=0,
        description=_('company type')
    )
    owner_uid = IntegerField(
        _('owner uid'),
        validators=[DataRequired()],
        default=0,
        description=_('owner uid')
    )
    status_delete = IntegerField(
        _('delete status'),
        validators=[DataRequired()],
        default=0,
        description=_('delete status')
    )
    delete_time = DateField(
        _('delete time'),
        validators=[DataRequired()],
        description=_('delete time')
    )
    create_time = DateField(
        _('create time'),
        validators=[DataRequired()],
        description=_('create time')
    )
    update_time = DateField(
        _('update time'),
        validators=[DataRequired()],
        description=_('update time')
    )


class CustomerEditForm(FlaskForm):
    """
    编辑表单（字段默认选项需要去除）
    """
    id = IntegerField(
        _('customer id'),
        validators=[
            DataRequired(),
        ],
        render_kw={
            'type': 'hidden',
        }
    )
    company_name = StringField(
        _('company name'),
        validators=[DataRequired(), Length(max=100)],
        description='公司名称，最大长度100字符'
    )
    company_address = StringField(
        _('company address'),
        validators=[DataRequired(), Length(max=100)],
        description='公司地址，最大长度100字符'
    )
    company_site = StringField(
        _('company site'),
        validators=[DataRequired(), Length(max=100)],
        description='公司官网，最大长度100字符'
    )
    company_tel = StringField(
        _('company tel'),
        validators=[DataRequired(), Length(max=100)],
        description='公司电话，最大长度100字符'
    )
    company_fax = StringField(
        _('company fax'),
        validators=[DataRequired(), Length(max=100)],
        description='公司传真，最大长度100字符'
    )
    company_type = IntegerField(
        _('company type'),
        validators=[DataRequired()],
        default=0,
        description=_('company type')
    )
    owner_uid = IntegerField(
        _('owner uid'),
        validators=[DataRequired()],
        default=0,
        description=_('owner uid')
    )
    create_time = DateField(
        _('create time'),
        validators=[DataRequired()],
        description=_('create time')
    )
    update_time = DateField(
        _('update time'),
        validators=[DataRequired()],
        description=_('update time')
    )
