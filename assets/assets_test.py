# coding=utf-8
"""
# @Time    : 10/14/19 4:37 PM
# @Author  : F0rGeEk@root
# @Email   : bat250@protonmail.com
# @File    : test_assets.py
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
import json
import time
import urllib.request
import urllib.parse
import os
import sys
from Conf import assets_setting

BASE_DIR = os.path.dirname(os.getcwd())
# 设置工作目录，使得包和模块能够正常导入
sys.path.append(BASE_DIR)


def update_test(data):
    """
    创建测试用例
    :return:
    """
    # 将数据打包到一个字典内，并转换为json格式
    data = {"assets_data": json.dumps(data)}
    # print(data)
    # 根据settings中的配置，构造url
    url = "http://%s:%s%s" % (assets_setting.Params['server'], assets_setting.Params['port'],
                              assets_setting.Params['url'])
    print('正在将数据发送至： [%s]  ......' % url)
    data_encode = urllib.parse.urlencode(data).encode()
    response = urllib.request.urlopen(url=url, data=data_encode, timeout=assets_setting.Params['request_timeout'])
    print("\033[31;1m发送完毕！\033[0m ")
    message = response.read().decode()
    print("返回结果：%s" % message)
    # try:
    #     # 使用Python内置的urllib.request库，发送post请求。
    #     # 需要先将数据进行封装，并转换成bytes类型
    #     data_encode = urllib.parse.urlencode(data).encode()
    #     response = urllib.request.urlopen(url=url, data=data_encode, timeout=assets_setting.Params['request_timeout'])
    #     print("\033[31;1m发送完毕！\033[0m ")
    #     message = response.read().decode()
    #     print("返回结果：%s" % message)
    # except Exception as e:
    #     message = "发送失败"
    #     print("\033[31;1m发送失败，%s\033[0m" % e)

    # 记录日志
    # with open(settings.PATH, 'ab') as f:
    with open(assets_setting.PATH, 'ab') as f:
        log = '发送时间： %s \t 服务器地址: %s \t 返回结果：%s \n' % (time.strftime('%Y-%m-%d %H-%M-%S'), url, message)
        f.write(log.encode())
        print('日志已记录完成！')


if __name__ == '__main__':
    windows_data = {
        "os_type": "Windows",
        "os_release": "2012 64bit R2",
        "os_distribution": "Microsoft",
        "assets_type": "server",
        "cpu_count": 8,
        "cpu_model": "Intel(R) Core(TM) i9-9750H CPU @ 4.30GHz",
        "cpu_core_count": 32,
        "ram": [
            {
                "slot": "A1",
                "volume": 128,
                "model": "Physical Memory",
                "brand": "kingstone ",
                "sn": "123426"
            },
            {
                "slot": "A2",
                "volume": 128,
                "model": "Physical Memory",
                "brand": "kingstone ",
                "sn": "123436"
            },

        ],
        "manufacturer": "Dell inc.",
        "model": "Y9320K 2018",
        "wake_up_type": 3,
        "sn": "31233-OEM-1212-132we3",
        "physical_disk_driver": [
            {
                "interface_type": "unknown",
                "slot": 0,
                "sn": "34567899123124566544",
                "model": "SAMSUNG SV134264G ATA Device",
                "brand": "希捷",
                "volume": 2048
            },
            {
                "interface_type": "SATA",
                "slot": 1,
                "sn": "312334565232365423",
                "model": "Seagate SV1124264G ATA Device",
                "brand": "希捷",
                "volume": 2048
            },

        ],
        "nic": [
            {
                "mac": "14:CF:22:EF:33:23",
                "model": "[00000032] Realtek RTL8192CU Wireless LAN 802.11n USB 2.0 Network Adapter",
                "name": 14,
                "ip_address": "10.8.8.15",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "0A:01:33:33:00:13",
                "model": "[00000331] VmWare WorkStation Host-Only Ethernet Adapter",
                "name": 24,
                "ip_address": "192.168.56.13",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "14:CF:22:FF:48:13",
                "model": "Intel Adapter",
                "name": 13,
                "ip_address": "192.1.1.13",
                "net_mask": ""
            },


        ]
    }

    linux_data = {
        "assets_type": "server",
        "manufacturer": "IBM.",
        "sn": "F3LN112",
        "model": "K1 Power S930",
        "uuid": "3334523-1234-4d12-804e-c6c2wwe31",
        "wake_up_type": "Power Switch",
        "os_distribution": "Ubuntu",
        "os_release": "Ubuntu 16.04.4 LTS",
        "os_type": "Linux",
        "cpu_count": "16",
        "cpu_core_count": "64",
        "cpu_model": "POWER 9E",
        "ram": [
            {
                "slot": "RAM slot #0",
                "volume": 128,
                "model": "Physical Memory",
                "brand": "IBM",
                "sn": "612212"
            }
        ],
        "size": 63.53899122970703,
        "nic": [],
        "physical_disk_driver": [
            {
                "model": "ST2245LM035-1RK015",
                "volume": "2048",
                    "sn": "WL23W25",
                "brand": "SanSung",
                "interface_type": "SATA"
            }
        ]
    }

    update_test(linux_data)
    update_test(windows_data)

