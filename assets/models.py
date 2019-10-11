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
    asset_manufacturer = models.ForeignKey('ManufacturerAssets', null=True, blank=True, verbose_name='厂商',
                                           on_delete=models.SET_NULL)
    asset_business = models.ForeignKey('BusinessAssets', null=True, blank=True, on_delete=models.SET_NULL,
                                       verbose_name='所属业务线')
    asset_manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP地址')
    asset_tags = models.ManyToManyField('TagAssets', blank=True, verbose_name='资产标签')
    asset_admin = models.ForeignKey('users.UserProfile', blank=True, related_name='asset_admin',
                                    verbose_name='资产管理员', on_delete=models.PROTECT)
    asset_idc = models.ForeignKey('IDCAssets', related_name='asset_idc', on_delete=models.PROTECT, null=True, blank=True,
                                  verbose_name='所在机房')
    asset_cabinet = models.ForeignKey('CabinetAssets', related_name='asset_cabinet', null=True, blank=True,
                                      verbose_name='所在机柜')
    asset_contract = models.ForeignKey('ContractAssets', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='合同')
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
        verbose_name_plural = verbose_name
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
        verbose_name_plural = verbose_name


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
        verbose_name_plural = verbose_name


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

    def __str__(self):
        return self.assets.asset_name + "--" + self.get_security_type_display() + str(self.security_model) + "id:%s" \
               % self.id

    class Meta:
        db_table = 'imu_security_assets'
        verbose_name = '安全设备资产表'
        verbose_name_plural = verbose_name


class StorageAssets(models.Model):
    """存储设备资源表"""
    storage_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储'),
        (2, '磁带库'),
        (3, '磁带机'),
        (4, '其他'),
    )
    assets = models.OneToOneField('Assets', on_delete=models.CASCADE)
    storage_type = models.SmallIntegerField(choices=storage_type_choice, default=4, verbose_name='存储类型')
    storage_sn = models.CharField(max_length=128, unique=True, verbose_name='设备序列号')
    storage_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='设备型号')
    storage_firmware = models.CharField(max_length=100, blank=True, null=True, verbose_name='固件版本')

    def __str__(self):
        return '%s--%s--%s<id:%s>' % (self.assets.asset_name, self.get_storage_type_display(), str(self.storage_model),
                                      self.id)

    class Meta:
        db_table = 'imu_storage_assets'
        verbose_name = '存储设备资产表'
        verbose_name_plural = verbose_name


class SoftAssets(models.Model):
    """软件类资产表"""
    soft_type_choice = (
        (0, '操作系统'),
        (1, '数据库授权'),
        (2, '网络相关授权'),
        (3, '办公/开发软件'),
        (4, '业务软件'),
        (5, '其他'),
    )
    assets = models.OneToOneField('Assets', on_delete=models.CASCADE)
    soft_type = models.SmallIntegerField(choices=soft_type_choice, default=5, verbose_name='软件资产类型')
    soft_license_num = models.IntegerField(max_length=100, default=1, verbose_name='授权数量')
    soft_version = models.CharField(max_length=100, blank=True, null=True, help_text="例如：Cent 5.2.9-2kali1",
                                    verbose_name='软件版本')

    def __str__(self):
        return '%s--%s--%s' % (self.assets.asset_name, self.get_soft_type_display(), self.soft_version)

    class Meta:
        db_table = 'imu_soft_assets'
        verbose_name = '软件资产表'
        verbose_name_plural = verbose_name


class OfficeAssets(models.Model):
    """办公相关设备资产表"""
    office_type_choice = (
        (0, '台式电脑'),
        (1, '笔记本'),
        (2, '打印机'),
        (3, '传真机'),
        (4, 'PAD'),
        (5, '手机'),
        (6, '电话'),
        (7, '其他'),
    )
    assets = models.OneToOneField('Assets', on_delete=models.CASCADE)
    office_type = models.CharField(choices=office_type_choice, default=7, verbose_name='办公设备类型')
    office_sn = models.CharField(max_length=128, unique=True, verbose_name='设备序列号')
    office_user = models.CharField(max_length=100, unique=True, editable=True, verbose_name='使用人')

    def __str__(self):
        return '%s--%s--%s' % (self.assets.asset_name, self.get_office_type_display(), self.office_user)

    class Meta:
        db_table = 'imu_office_assets'
        verbose_name = '办公设备资产表'
        verbose_name_plural = verbose_name


class ManufacturerAssets(models.Model):
    """厂商信息表"""
    manufacturer_name = models.CharField(max_length=100, unique=True, verbose_name='厂商名称')
    manufacturer_contacts = models.CharField(max_length=100, verbose_name='厂商联系人')
    manufacturer_phone = models.CharField(max_length=11, null=True, unique=True, verbose_name="联系人电话")
    manufacturer_email = models.EmailField(unique=True, verbose_name='联系邮箱')
    manufacturer_memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return '%s--%s' % (self.manufacturer_name, self.manufacturer_contacts)

    class Meta:
        db_table = 'imu_manufacturer_assets'
        verbose_name = '厂商信息表'
        verbose_name_plural = verbose_name


class BusinessAssets(models.Model):
    """业务线"""
    business_name = models.CharField(max_length=100, unique=True, verbose_name='业务线名称')
    business_charge = models.ForeignKey('users.UserProfile', blank=True, verbose_name='业务负责人',
                                        on_delete=models.PROTECT)
    business_department = models.CharField(max_length=100, blank=True, verbose_name='所属部门')

    def __str__(self):
        return self.business_name + self.business_department

    class Meta:
        db_table = 'imu_business_assets'
        verbose_name = '业务线资产表'
        verbose_name_plural = verbose_name


class TagAssets(models.Model):
    """资产标签表"""
    tag_name = models.CharField(max_length=32, unique=True, verbose_name='标签名')
    tag_c_day = models.DateField(auto_now_add=True, verbose_name='创建日期')

    def __str__(self):
        return self.tag_name

    class Meta:
        db_table = 'imu_tag_assets'
        verbose_name = "标签"
        verbose_name_plural = verbose_name


