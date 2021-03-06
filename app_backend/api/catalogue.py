#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: catalogue.py
@time: 2018-04-06 18:23
"""

from app_backend.databases.bearing import db_bearing
from app_backend.models.model_bearing import Catalogue
from app_common.libs.mysql_orm_op import DbInstance

db_instance = DbInstance(db_bearing)


def get_catalogue_row_by_id(catalogue_id):
    """
    通过 id 获取信息
    :param catalogue_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Catalogue, catalogue_id)


def get_catalogue_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Catalogue, *args, **kwargs)


def get_catalogue_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Catalogue, *args, **kwargs)


def get_catalogue_limit_rows_by_last_id(last_pk_id, limit_num, *args, **kwargs):
    """
    通过最后一个主键 id 获取最新信息列表
    :param last_pk_id:
    :param limit_num:
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_limit_rows_by_last_id(Catalogue, last_pk_id, limit_num, *args, **kwargs)


def add_catalogue(catalogue_data):
    """
    添加信息
    :param catalogue_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Catalogue, catalogue_data)


def edit_catalogue(catalogue_id, catalogue_data):
    """
    修改信息
    :param catalogue_id:
    :param catalogue_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Catalogue, catalogue_id, catalogue_data)


def delete_catalogue(catalogue_id):
    """
    删除信息
    :param catalogue_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(Catalogue, catalogue_id)


def get_catalogue_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(Catalogue, page, per_page, *args, **kwargs)
    return rows


def delete_catalogue_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(Catalogue)


def count_catalogue(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(Catalogue, *args, **kwargs)


def insert_rows(data_list):
    """
    批量插入
    :param data_list:
    :return:
    """
    return db_instance.insert_rows(Catalogue, data_list)


def get_catalogue_choices(keywords):
    """
    获取选项
    :param keywords:
    :return:
    """

    from app_backend.clients.client_es import es_client
    from app_common.libs.es import ES

    es = ES(es_client)

    index = 'catalogue'
    doc_type = 'bearing'
    # field = 'product_label'
    field = 'product_model'
    # keywords = '7008ACDGA/P4A'
    query_from = 0
    size = 0

    es_result = es.search_fulltext(index, doc_type, field, keywords, query_from, size)

    catalogue_choices = map(lambda x: (
        x['id'], x['value'], '%s <small class="text-muted">%s</small>' % (x['label'], x['info']['product_brand']),
        x['info']['product_brand']), es_result['data'])
    return catalogue_choices
