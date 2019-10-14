# coding=utf-8
"""
# @Time    : 10/14/19 4:01 PM
# @Author  : F0rGeEk@root
# @Email   : bat250@protonmail.com
# @File    : main.py
# @Software: PyCharm
***********************************************************
███████╗ ██████╗ ██████╗  ██████╗ ███████╗███████╗██╗  ██╗
██╔════╝██╔═████╗██╔══██╗██╔════╝ ██╔════╝██╔════╝██║ ██╔╝
█████╗  ██║██╔██║██████╔╝██║  ███╗█████╗  █████╗  █████╔╝ 
██╔══╝  ████╔╝██║██╔══██╗██║   ██║██╔══╝  ██╔══╝  ██╔═██╗ 
██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗███████╗██║  ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
***********************************************************
"""
import os
import sys
from test.core import handler


BASE_DIR = os.path.dirname(os.getcwd())
print('base dir is %s' % BASE_DIR)

# 设置工作目录
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    handler.ArgvHandler(sys.argv)
