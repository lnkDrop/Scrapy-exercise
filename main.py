#!/usr/bin/env python
# encoding: utf-8
from scrapy.cmdline import execute

import sys
import os

# print(__file__)
# 项目根目录绝对路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "cnblogs"])
