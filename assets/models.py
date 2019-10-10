from django.db import models


class Assets(models.Model):
    """资产共有属性表"""
    # 资产类型
    asset_types = (
        ('server', '服务器'),
        ('network', '网络设备'),
        ('storage', '存储设备'),
        ('security', '安全设备'),
        ('software', '软件资产'),
        ('office', '办公设备'),
        ('other', '其他设备'),
    )
    # 资产状态
    asset_status = (
        ('0', '在线'),
        ('1', '下线'),
        ('2', '故障'),
        ('3', '备用'),
        ('4', '未知'),
    )

    asset_types = models.CharField(choices=asset_types, max_length=64, default='other', verbose_name='资产类型')
    asset_sn = models.CharField(max_length=128, unique=True, verbose_name='资产编号')
    asset_name = models.CharField(max_length=64, unique=True, editable=True, verbose_name='资产名称')
    asset_status = models.SmallIntegerField(choices=asset_status, default=4, verbose_name='资产状态')
    asset_manufacturer = models.ForeignKey('AssetManufacturer', null=True, blank=True, verbose_name='厂商',
                                           on_delete=models.SET_NULL)
    asset_business = models.ForeignKey('AssetBusiness', null=True, blank=True, on_delete=models.SET_NULL,
                                       verbose_name='所属业务线')
    asset_manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP地址')
    asset_tags = models.ManyToManyField('AssetTag', blank=True, verbose_name='资产标签')
    asset_admin = models.ForeignKey('users.UserProfile', blank=True, related_name='asset_admin',
                                    verbose_name='资产管理员', on_delete=models.PROTECT)
    asset_idc = models.ForeignKey('IDC', related_name='asset_idc', on_delete=models.PROTECT, null=True, blank=True,
                                  verbose_name='所在机房')
    asset_cabinet = models.ForeignKey('Cabinet', related_name='asset_cabinet', null=True, blank=True,
                                      verbose_name='所在机柜')
    asset_contract = models.ForeignKey('Contract', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='合同')
    asset_purchase_day = models.DateField(null=True, blank=True, verbose_name='购买日期')
    asset_expire_day = models.DateField(null=True, blank=True, verbose_name='过保日期')
    asset_price = models.CharField(max_length=100, null=True, blank=True, verbose_name='价格(RMB)')
    asset_approved = models.ForeignKey('users.UserProfile', null=True, blank=True, related_name='asset_approved',
                                       on_delete=models.SET_NULL, verbose_name='批准人')
    asset_c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准时间')
    asset_u_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    asset_memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return '<%s> %s' % (self.get_asset_types_display(), self.asset_name)

    class Meta:
        da_table = 'imu_assets'
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'
        ordering = ['-c_time']


class ServerAssets(models.Model):
    """服务器资产表"""
    server_type_choice = (
        (0, '塔式服务器'),
        (1, '刀片服务器'),
        (2, '机架式服务器'),
        (3, '虚拟机'),
        (4, '容器'),
        (5, '云主机'),
    )
    server_create_by_choice = (
        ('auto', '自动发现'),
        ('manual', '手工录入'),
        ('batch', '批量导入'),
    )
    # 一对一关联，assets删除时同时删除ServerAssets
    assets = models.OneToOneField('Assets', on_delete=models.CASCADE)
    server_type = models.SmallIntegerField(choices=server_type_choice, default=2, verbose_name="服务器类型")
    server_create_by = models.CharField(choices=server_create_by_choice, max_length=32, default='manual',
                                        verbose_name='添加方式')
    server_hostname = models.CharField(max_length=100, unique=True, editable=True, verbose_name='主机名')
    server_sn = models.CharField(max_length=128, unique=True, verbose_name='序列号')
    server_host_on = models.ForeignKey('self', related_name='host_on_server', blank=True, null=True,
                                       verbose_name='宿主机', on_delete=models.CASCADE)
    server_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='服务器型号')
    server_raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='RAID卡类型')
    server_os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作系统类型')
    server_os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name='发行商')
    server_os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name='内核版本')

    def __str__(self):
        return '%s--%s--%s--<assets_sn:%s>' % (self.assets.asset_name, self.get_server_type_display(),
                                               self.server_model, self.assets.asset_sn)

    class Meta:
        db_table = 'imu_server_assets'
        verbose_name = '服务器资产表'
        verbose_name_plural = '服务器资产表'


class NetworkAssets(models.Model):
    """网络设备资产表"""
    network_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, 'WLC'),
        (3, 'AP'),
        (4, '流量控制'),
    )
    assets = models.OneToOneField('Assets', on_delete=models.CASCADE)
    network_type = models.SmallIntegerField(choices=network_type_choice, default=1, verbose_name='设备类型')
    network_sn = models.CharField(max_length=128, unique=True, verbose_name='设备序列号')
    network_hostname = models.CharField(max_length=100, unique=True, editable=True, verbose_name='主机名')
    network_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='设备型号')
    network_port_num = models.IntegerField(max_length=100, blank=True, null=True, verbose_name='端口数')
    network_firmware = models.CharField(max_length=100, blank=True, null=True, verbose_name='固件版本')

    def __str__(self):
        return '%s--%s--%s--<assets_sn:%s>' % (self.assets.asset_name, self.get_network_type_display(),
                                               self.network_model, self.assets.asset_sn)

    class Meta:
        db_table = 'imu_network_assets'
        verbose_name = '网络设备资产表'
        verbose_name_plural = '网络设备资产表'


class SecurityAssets(models.Model):
    """安全设备资产表"""
    security_type_choice = (
        (0, 'FireWall'),
        (1, 'IPS'),
        (2, 'IDS'),
        (3, 'vpn'),
        (4, 'AD'),
        (5, 'AC'),
        (6, 'WAF'),
        (7, 'DBScan'),
        (8, 'AES'),
        (9, 'other'),
    )
    assets = models.OneToOneField('Assets', on_delete=models.CASCADE)
    security_type = models.SmallIntegerField(choices=security_type_choice, default=9, verbose_name='产品类型')
    security_sn = models.CharField(max_length=128, unique=True, verbose_name='设备序列号')
    security_hostname = models.CharField(max_length=100, unique=True, editable=True, verbose_name='主机名')
    security_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='设备型号')
    security_firmware = models.CharField(max_length=100, blank=True, null=True, verbose_name='固件版本')

    class Meta:
        db_table = 'imu_security_assets'
        verbose_name = '安全设备资产表'
        verbose_name_plural = '安全设备资产表'



