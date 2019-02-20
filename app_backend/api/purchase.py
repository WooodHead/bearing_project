#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: purchase.py
@time: 2018-07-27 20:07
"""

from copy import copy
from datetime import datetime
from sqlalchemy.sql import func
from app_backend import db
from app_backend.api.customer import get_customer_rows_by_ids
from app_backend.api.user import get_user_rows_by_ids
from app_common.libs.mysql_orm_op import DbInstance
from app_backend.models.bearing_project import Purchase
from app_common.maps.default import default_choices_int
from app_common.maps.status_delete import STATUS_DEL_NO
from app_common.tools.date_time import get_current_day_time_ends, get_hours, time_local_to_utc, \
    get_current_month_time_ends, get_days, get_current_year_time_ends, get_months
from app_common.maps.status_order import STATUS_ORDER_OK

db_instance = DbInstance(db)


def get_purchase_row_by_id(purchase_id):
    """
    通过 id 获取信息
    :param purchase_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Purchase, purchase_id)


def get_purchase_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Purchase, *args, **kwargs)


def get_purchase_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Purchase, *args, **kwargs)


def add_purchase(purchase_data):
    """
    添加信息
    :param purchase_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Purchase, purchase_data)


def edit_purchase(purchase_id, purchase_data):
    """
    修改信息
    :param purchase_id:
    :param purchase_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Purchase, purchase_id, purchase_data)


def delete_purchase(purchase_id):
    """
    删除信息
    :param purchase_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(Purchase, purchase_id)


def delete_purchase_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(Purchase)


def count_purchase(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(Purchase, *args, **kwargs)


def get_purchase_pagination(page=1, per_page=10, *args, **kwargs):
    """
    获取列表（分页）
    Usage:
        items: 信息列表
        has_next: 如果本页之后还有超过一个分页，则返回True
        has_prev: 如果本页之前还有超过一个分页，则返回True
        next_num: 返回下一页的页码
        prev_num: 返回上一页的页码
        iter_pages(): 页码列表
        iter_pages(left_edge=2, left_current=2, right_current=5, right_edge=2) 页码列表默认参数
    :param page:
    :param per_page:
    :param args:
    :param kwargs:
    :return:
    """
    rows = db_instance.get_pagination(Purchase, page, per_page, *args, **kwargs)
    return rows


def get_distinct_purchase_uid(*args, **kwargs):
    """
    获取用户
    :param args:
    :param kwargs:
    :return: List
    """
    field = 'uid'
    return map(lambda x: getattr(x, field), db_instance.get_distinct_field(Purchase, field, *args, **kwargs))


def get_purchase_user_list_choices():
    purchase_user_list = copy(default_choices_int)
    uid_list = get_distinct_purchase_uid(status_delete=STATUS_DEL_NO)
    user_rows = get_user_rows_by_ids(uid_list)
    purchase_user_list.extend([(user.id, user.name) for user in user_rows])
    return purchase_user_list
