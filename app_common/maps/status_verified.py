#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: status_verified.py
@time: 2018-03-18 03:02
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

# 认证状态（0:未认证，1:已认证）
STATUS_VERIFIED_NO = 0
STATUS_VERIFIED_OK = 1

STATUS_VERIFIED_DICT = {
    STATUS_VERIFIED_NO: _('Not Verified'),  # 未认证
    STATUS_VERIFIED_OK: _('Verified'),  # 已认证
}
