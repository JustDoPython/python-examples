#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-05-31 17:25

@author: cxhuan
"""


class StockUtils:
    @staticmethod
    def calc_limit_price(pre_close):
        try:
            if pre_close == 0:
                return 0

            limit = pre_close + pre_close*0.1
            limit = '%.2f' % limit
            return limit
        except Exception:
            return 0.00



