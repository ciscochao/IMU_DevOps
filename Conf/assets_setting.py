# coding=utf-8
"""
# @Time    : 10/17/19 1:49 PM
# @Author  : F0rGeEk@root
# @Email   : bat250@protonmail.com
# @File    : assets_setting.py
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

# 远端接收数据的服务器
Params = {
    "server": "127.0.0.1",
    "port": 8000,
    'url': '/assets/report/',
    'request_timeout': 30,
}

# 日志文件配置

# PATH = os.path.join(os.path.dirname(os.getcwd()), 'IMU_DevOps', 'test', './Log', 'IMU_assets.log')
PATH = "/root/Python/Projects/IMU_DevOps/Log/CMDB.log"


