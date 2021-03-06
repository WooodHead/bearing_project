#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: status_order.py
@time: 2018-04-05 22:55
"""

from __future__ import unicode_literals

from flask_babel import lazy_gettext as _

# 订单状态（0:等待下单,1:下单成功,2:下单失败）
STATUS_ORDER_NO = 0
STATUS_ORDER_OK = 1
STATUS_ORDER_ER = 2

STATUS_ORDER_DICT = {
    STATUS_ORDER_NO: _('Pending Order'),  # 等待下单
    STATUS_ORDER_OK: _('Order Success'),  # 下单成功
    STATUS_ORDER_ER: _('Order Failure'),  # 下单失败
}

STATUS_ORDER_CHOICES = STATUS_ORDER_DICT.items()
