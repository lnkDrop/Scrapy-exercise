#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/20 10:39
# @Author : inkDrop
# @Site : 
# @File : common.py
# @Software: PyCharm

# MD5加密缩短url长度
import hashlib


def get_Md5(url):
    if isinstance(url, str):
        # 字符串转换
        url = url.encode("utf-8")
    # md5加密
    m = hashlib.md5()
    m.update(url)

    return m.hexdigest()

if __name__ == '__main__':
    print(get_Md5("http://cnblogs.com"))