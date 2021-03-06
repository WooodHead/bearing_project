#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2019-05-12 09:58
"""

from __future__ import unicode_literals

from functools import partial

from app_backend.permissions import SectionNeed, SectionActionNeed, BasePermission

# -------------------------------------------------------------
# 库存板块整体权限
InventorySectionNeed = partial(SectionNeed, 'inventory')
permission_inventory_section = BasePermission(InventorySectionNeed())

# -------------------------------------------------------------
# 库存板块操作权限（创建、查询、统计、导出、详情、编辑、删除、审核、打印）
InventorySectionActionNeed = partial(SectionActionNeed, 'inventory')
InventorySectionActionNeed.__doc__ = """A need with the section preset to `"inventory"`."""

permission_inventory_section_add = BasePermission(InventorySectionActionNeed('add'))
permission_inventory_section_search = BasePermission(InventorySectionActionNeed('search'))
permission_inventory_section_stats = BasePermission(InventorySectionActionNeed('stats'))
permission_inventory_section_export = BasePermission(InventorySectionActionNeed('export'))

permission_inventory_section_get = BasePermission(InventorySectionActionNeed('get'))
permission_inventory_section_edit = BasePermission(InventorySectionActionNeed('edit'))
permission_inventory_section_del = BasePermission(InventorySectionActionNeed('del'))
permission_inventory_section_audit = BasePermission(InventorySectionActionNeed('audit'))
permission_inventory_section_print = BasePermission(InventorySectionActionNeed('print'))
