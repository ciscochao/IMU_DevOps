# coding=utf-8
"""
# @Time    : 10/16/19 5:34 PM
# @Author  : F0rGeEk@root
# @Email   : bat250@protonmail.com
# @File    : assets_handler.py
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
from assets import models


class NewAssets(object):
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def add_to_new_assets_zone(self):
        defaults = {
            'data': json.dumps(self.data),
            'assets_type': self.data.get('assets_type'),
            'manufacturer': self.data.get('manufacturer'),
            'model': self.data.get('model'),
            # 'volume': self.data.get(),
            'cpu_model': self.data.get('cpu_model'),
            'cpu_count': self.data.get('cpu_count'),
            'cpu_core_count': self.data.get('cpu_core_count'),
            'os_distribution': self.data.get('os_distribution'),
            'os_release': self.data.get('os_release'),
            'os_type': self.data.get('os_type'),
        }
        ram_volume = 0
        ram = self.data.get('ram')
        for i in range(len(ram)):
            ram_volume += ram[i].get('volume')
        models.NewAssetApprovalZone.objects.update_or_create(sn=self.data['sn'], defaults=defaults,
                                                             ram_volume=ram_volume)
        # models.NewAssetApprovalZone.objects.update_or_create(sn=self.data['sn'], defaults=defaults)

        return '资产已加入或更新至待审批区！'


class ApproveAssets:
    # 审批待上线资产
    def __init__(self, request, assets_id):
        self.request = request
        self.new_assets = models.NewAssetApprovalZone.objects.get(id=assets_id)
        self.data = json.loads(self.new_assets.data)

    def assets_online(self):
        # 预留接口
        func = getattr(self, "_%s_online" % self.new_assets.assets_type)
        ret = func()
        return ret

    def _server_online(self):
        assets = self._create_assets()
        try:
            self._create_manufacturer(assets)  # 创建厂商
            self._create_server(assets)  # 创建服务器
            self._create_cpu(assets)  # 创建CPU
            self._create_ram(assets)  # 创建内存
            self._create_disk(assets)  # 创建硬盘
            self._create_nic(assets)  # 创建网卡
            self._delete_original_asset()  # 从待审批资产区删除已审批上线的资产
        except Exception as e:
            assets.delete()
            log('approve_failed', msg=e, new_assets=self.new_assets, request=self.request)
            print(e)
            return False
        else:
            # 添加日志
            log("online", assets=assets, request=self.request)
            print("新服务器上线!")
            return True

    def _create_assets(self):
        # 创建资产并上线
        assets = models.Assets.objects.create(assets_type=self.new_assets.assets_type,
                                              assets_name="%s:%s" % (self.new_assets.assets_type, self.new_assets.sn),
                                              sn=self.new_assets.sn, assets_approved=self.request.user,)
        return assets

    def _create_manufacturer(self, asset):
        # 创建厂商
        m = self.new_assets.manufacturer
        if m:
            manufacturer_obj, _ = models.ManufacturerAssets.objects.get_or_create(name=m)
            asset.manufacturer = manufacturer_obj
            asset.save()

    def _create_server(self, asset):
        # 创建服务器
        models.ServerAssets.objects.create(assets=asset, model=self.new_assets.model, os_type=self.new_assets.os_type,
                                           os_distribution=self.new_assets.os_distribution,
                                           os_release=self.new_assets.os_release)

    def _create_cpu(self, asset):
        # 创建CPU
        cpu = models.CPUAssets.objects.create(assets=asset)
        cpu.cpu_model = self.new_assets.cpu_model
        cpu.cpu_count = self.new_assets.cpu_count
        cpu.cpu_core_count = self.new_assets.cpu_core_count
        cpu.save()

    def _create_ram(self, asset):
        # 创建内存
        ram_list = self.data.get('ram')
        if not ram_list:
            return
        for ram_dict in ram_list:
            if not ram_dict.get('slot'):
                raise ValueError("内存插槽位置不存在！")
            ram = models.RAMAssets()
            ram.assets = asset
            ram.slot = ram_dict.get('slot')
            ram.sn = ram_dict.get('sn')
            ram.model = ram_dict.get('model')
            ram.manufacturer = ram_dict.get('manufacturer')
            ram.volume = ram_dict.get('volume', 0)
            ram.save()

    def _create_disk(self, asset):
        # 创建硬盘
        disk_list = self.data.get('physical_disk_driver')
        if not disk_list:  # 一条硬盘数据都没有
            return
        for disk_dict in disk_list:
            if not disk_dict.get('sn'):
                raise ValueError("未知sn的硬盘！")  # 根据sn确定具体某块硬盘。
            disk = models.DiskAssets()
            disk.assets = asset
            disk.sn = disk_dict.get('sn')
            disk.model = disk_dict.get('model')
            disk.brand = disk_dict.get('brand'),
            disk.slot = disk_dict.get('slot')
            disk.volume = disk_dict.get('volume', 0)
            iface = disk_dict.get('interface_type')
            if iface in ['SATA', 'SAS', 'SCSI', 'SSD', 'unknown']:
                disk.interface_type = iface

            disk.save()

    def _create_nic(self, asset):
        # 创建网卡
        nic_list = self.data.get("nic")
        if not nic_list:
            return

        for nic_dict in nic_list:
            if not nic_dict.get('mac'):
                raise ValueError("网卡缺少mac地址！")
            if not nic_dict.get('model'):
                raise ValueError("网卡型号未知！")

            nic = models.NICAssets()
            nic.assets = asset
            nic.name = nic_dict.get('name')
            nic.model = nic_dict.get('model')
            nic.mac = nic_dict.get('mac')
            nic.ip_address = nic_dict.get('ip_address')
            if nic_dict.get('net_mask'):
                if len(nic_dict.get('net_mask')) > 0:
                    nic.net_mask = nic_dict.get('net_mask')[0]
            nic.save()

    def _delete_original_asset(self):
        # 对审批通过的资产进行待审批区删除
        self.new_assets.delete()


class UpdateAssets:
    # 更新已上线资产信息
    def __init__(self, request, assets, report_data):
        self.request = request
        self.assets = assets
        self.report_data = report_data
        self.asset_update()

    def asset_update(self):
        # 预留接口
        func = getattr(self, "_%s_update" % self.report_data['assets_type'])
        ret = func()
        return ret

    def _server_update(self):
        try:
            self._update_manufacturer()  # 更新厂商
            self._update_server()  # 更新服务器
            self._update_cpu()  # 更新CPU
            self._update_ram()  # 更新内存
            self._update_disk()  # 更新硬盘
            self._update_nic()  # 更新网卡
            self.assets.save()
        except Exception as e:
            log('update_failed', msg=e, assets=self.assets, request=self.request)
            print(e)
            return False
        else:
            # 添加日志
            log("update_success", assets=self.assets)
            print("资产数据被更新!")
            return True

    def _update_manufacturer(self):
        # 更新厂商

        m = self.report_data.get('manufacturer')
        if m:
            manufacturer_obj, _ = models.ManufacturerAssets.objects.get_or_create(name=m)
            self.assets.manufacturer = manufacturer_obj
        else:
            self.assets.manufacturer = None
        self.assets.manufacturer.save()

    def _update_server(self):
        # 更新服务器
        self.assets.serverassets.model = self.report_data.get('model')
        self.assets.serverassets.os_type = self.report_data.get('os_type')
        self.assets.serverassets.os_distribution = self.report_data.get('os_distribution')
        self.assets.serverassets.os_release = self.report_data.get('os_release')
        self.assets.serverassets.save()

    def _update_cpu(self):
        # 更新CPU信息
        self.assets.cpu_assets .cpu_model = self.report_data.get('cpu_model')
        self.assets.cpu_assets.cpu_count = self.report_data.get('cpu_count')
        self.assets.cpu_assets.cpu_core_count = self.report_data.get('cpu_core_count')
        self.assets.cpu_assets.save()

    def _update_ram(self):
        """
        更新内存信息。
        使用集合数据类型中差的概念，处理不同的情况。
        如果新数据有，但原数据没有，则新增；
        如果新数据没有，但原数据有，则删除原来多余的部分；
        如果新的和原数据都有，则更新。
        在原则上，下面的代码应该写成一个复用的函数，
        但是由于内存、硬盘、网卡在某些方面的差别，导致很难提取出重用的代码。
        :return:
        """
        # 获取已有内存信息，并转成字典格式
        old_rams = models.RAMAssets.objects.filter(assets=self.assets)
        old_rams_dict = dict()
        if old_rams:
            for ram in old_rams:
                old_rams_dict[ram.slot] = ram
        # 获取新数据中的内存信息，并转成字典格式
        new_rams_list = self.report_data['ram']
        new_rams_dict = dict()
        if new_rams_list:
            for item in new_rams_list:
                new_rams_dict[item['slot']] = item

        # 利用set类型的差集功能，获得需要删除的内存数据对象
        need_deleted_keys = set(old_rams_dict.keys()) - set(new_rams_dict.keys())
        if need_deleted_keys:
            for key in need_deleted_keys:
                old_rams_dict[key].delete()

        # 需要新增或更新的
        if new_rams_dict:
            for key in new_rams_dict:
                defaults = {
                    'sn': new_rams_dict[key].get('sn'),
                    'model': new_rams_dict[key].get('model'),
                    'brand': new_rams_dict[key].get('brand'),
                    'volume': new_rams_dict[key].get('volume', 0),
                }
                models.RAMAssets.objects.update_or_create(assets=self.assets, slot=key, defaults=defaults)

    def _update_disk(self):
        """
        更新硬盘信息,类似更新内存。
        """
        old_disks = models.DiskAssets.objects.filter(assets=self.assets)
        old_disks_dict = dict()
        if old_disks:
            for disk in old_disks:
                old_disks_dict[disk.sn] = disk

        new_disks_list = self.report_data['physical_disk_driver']
        new_disks_dict = dict()
        if new_disks_list:
            for item in new_disks_list:
                new_disks_dict[item['sn']] = item

        # 需要删除的
        need_deleted_keys = set(old_disks_dict.keys()) - set(new_disks_dict.keys())
        if need_deleted_keys:
            for key in need_deleted_keys:
                old_disks_dict[key].delete()

        # 需要新增或更新的
        if new_disks_dict:
            for key in new_disks_dict:
                interface_type = new_disks_dict[key].get('interface_type', 'unknown')
                if interface_type not in ['SATA', 'SAS', 'SCSI', 'SSD', 'unknown']:
                    interface_type = 'unknown'
                defaults = {
                    'slot': new_disks_dict[key].get('slot'),
                    'model': new_disks_dict[key].get('model'),
                    'brand': new_disks_dict[key].get('brand'),
                    'volume': new_disks_dict[key].get('volume', 0),
                    'interface_type': interface_type,
                }
                models.DiskAssets.objects.update_or_create(assets=self.assets, sn=key, defaults=defaults)

    def _update_nic(self):
        """
        更新网卡信息,类似更新内存。
        """
        old_nics = models.NICAssets.objects.filter(assets=self.assets)
        old_nics_dict = dict()
        if old_nics:
            for nic in old_nics:
                old_nics_dict[nic.model + nic.mac] = nic

        new_nics_list = self.report_data['nic']
        new_nics_dict = dict()
        if new_nics_list:
            for item in new_nics_list:
                new_nics_dict[item['model'] + item['mac']] = item

        # 需要删除的
        need_deleted_keys = set(old_nics_dict.keys()) - set(new_nics_dict.keys())
        if need_deleted_keys:
            for key in need_deleted_keys:
                old_nics_dict[key].delete()

        # 需要新增或更新的
        if new_nics_dict:
            for key in new_nics_dict:
                if new_nics_dict[key].get('net_mask') and len(new_nics_dict[key].get('net_mask')) > 0:
                    net_mask = new_nics_dict[key].get('net_mask')[0]
                else:
                    net_mask = ""
                defaults = {
                    'name': new_nics_dict[key].get('name'),
                    'ip_address': new_nics_dict[key].get('ip_address'),
                    'net_mask': net_mask,
                }
                models.NICAssets.objects.update_or_create(assets=self.assets, model=new_nics_dict[key]['model'],
                                                          mac=new_nics_dict[key]['mac'], defaults=defaults)

        print('更新成功！')


def log(log_type, msg=None, assets=None, new_assets=None, request=None):
    # 记录日志
    event = models.EventLog()
    if log_type == "online":
        event.name = "%s <%s> ：  上线" % (assets.assets_name, assets.sn)
        event.assets = assets
        event.detail = "资产成功上线！"
        event.user = request.user
    elif log_type == "approve_failed":
        event.name = "%s <%s> ：  审批失败" % (new_assets.assets_type, new_assets.sn)
        event.new_assets = new_assets
        event.detail = "审批失败！\n%s" % msg
        event.user = request.user
    elif log_type == "update_success":
        event.name = "%s [%s] <%s> ：  数据更新！" % (assets.assets_type, assets.assets_name, assets.sn)
        event.assets = assets
        event.detail = "更新成功！"
    elif log_type == "update_failed":
        event.name = "%s [%s] <%s> ：  更新失败" % (assets.assets_type, assets.assets_name, assets.sn)
        event.assets = assets
        event.detail = "更新失败！\n%s" % msg
        # 更多日志类型.....
    event.save()
