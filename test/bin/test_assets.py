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
from test.conf import settings

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
    # 根据settings中的配置，构造url
    url = "http://%s:%s%s" % (settings.Params['server'], settings.Params['port'], settings.Params['url'])
    print('正在将数据发送至： [%s]  ......' % url)
    try:
        # 使用Python内置的urllib.request库，发送post请求。
        # 需要先将数据进行封装，并转换成bytes类型
        data_encode = urllib.parse.urlencode(data).encode()
        response = urllib.request.urlopen(url=url, data=data_encode, timeout=settings.Params['request_timeout'])
        print("\033[31;1m发送完毕！\033[0m ")
        message = response.read().decode()
        print("返回结果：%s" % message)
    except Exception as e:
        message = "发送失败"
        print("\033[31;1m发送失败，%s\033[0m" % e)

    # 记录日志
    # with open(settings.PATH, 'ab') as f:
    with open(settings.PATH, 'ab') as f:
        log = '发送时间： %s \t 服务器地址: %s \t 返回结果：%s \n' % (time.strftime('%Y-%m-%d %H-%M-%S'), url, message)
        f.write(log.encode())
        print('日志已记录完成！')


if __name__ == '__main__':
    windows_data = {
        "sn": "test_windows_1",
        "server_os_type": "Windows",
        "server_os_release": "2018 64bit R2",
        "server_os_distribution": "Microsoft",
        "assets_type": "server",
        "cpu_count": 8,
        "cpu_model": "Intel(R) Core(TM) i7-9750H CPU @ 2.80GHz",
        "cpu_core_count": 32,
        "ram": [
            {
                "ram_slot": "A1",
                "ram_volume": 64,
                "ram_model": "Physical Memory",
                "ram_brand": "kingstone ",
                "ram_sn": "123456"
            },

        ],
        "assets_manufacturer": "Dell inc.",
        "server_model": "Y9320K 2019",
        "wake_up_type": 3,
        "server_sn": "31233-OEM-8992662-1321122",
        "physical_disk_driver": [
            {
                "iface_type": "unknown",
                "disk_slot": 0,
                "disk_sn": "34567899234456276543234234566544",
                "disk_model": "SAMSUNG SV100S264G ATA Device",
                "disk_brand": "(标准磁盘驱动器)",
                "disk_volume": 1024
            },
            {
                "iface_type": "SATA",
                "disk_slot": 1,
                "disk_sn": "3123345654323456787654334765423",
                "disk_model": "Seagate SV100S264G ATA Device",
                "disk_brand": "(标准磁盘驱动器)",
                "disk_volume": 1024
            },

        ],
        "nic": [
            {
                "nic_mac": "14:CF:22:EF:33:12",
                "nic_model": "[00000033] Realtek RTL8192CU Wireless LAN 802.11n USB 2.0 Network Adapter",
                "nic_name": 14,
                "nic_ip_address": "10.8.8.14",
                "nic_net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "nic_mac": "0A:01:33:33:00:14",
                "nic_model": "[00000333] VmWare WorkStation Host-Only Ethernet Adapter",
                "nic_name": 24,
                "nic_ip_address": "192.168.56.14",
                "nic_net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "nic_mac": "14:CF:22:FF:48:14",
                "nic_model": "Intel Adapter",
                "nic_name": 14,
                "nic_ip_address": "192.1.1.14",
                "nic_net_mask": ""
            },


        ]
    }

    linux_data = {
        "sn": "test_linux_1",
        "assets_type": "server",
        "assets_manufacturer": "IBM.",
        "server_sn": "F3LN110",
        "server_model": "K1 Power S930",
        "uuid": "4c4c4523-0039-4d20-804e-c6c2wwe31",
        "wake_up_type": "Power Switch",
        "server_os_distribution": "Ubuntu",
        "server_os_release": "Ubuntu 16.04.4 LTS",
        "server_os_type": "Linux",
        "cpu_count": "8",
        "cpu_core_count": "32",
        "cpu_model": "POWER 9",
        "ram": [
            {
                "ram_slot": "RAM slot #0",
                "ram_volume": 64,
                "ram_model": "Physical Memory",
                "ram_brand": "IBM",
                "ram_sn": "623466"
            }
        ],
        "ram_size": 63.538997344970703,
        "nic": [],
        "physical_disk_driver": [
            {
                "disk_model": "ST1033LM035-1RK015",
                "disk_volume": "1024",
                "disk_sn": "WL109C15",
                "disk_brand": "SanSung",
                "disk_interface_type": "IDE"
            }
        ]
    }

    update_test(linux_data)
    update_test(windows_data)

