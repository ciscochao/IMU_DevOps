from django.db import models
from django.contrib.auth.models import User


class Assets(models.Model):
    """资产共有属性表"""
    # 资产类型
    assets_type = (
        ('server', '服务器'),
        ('network', '网络设备'),
        ('storage', '存储设备'),
        ('security', '安全设备'),
        ('software', '软件资产'),
        ('office', '办公设备'),
        ('other', '其他设备'),
    )
    # 资产状态
    assets_status = (
        ('0', '在线'),
        ('1', '下线'),
        ('2', '故障'),
        ('3', '备用'),
        ('4', '未知'),
    )

    assets_type = models.CharField(choices=assets_type, max_length=64, default='other', verbose_name='资产类型')
    assets_num = models.CharField(max_length=128, unique=True, null=True, verbose_name='资产编号')
    sn = models.CharField(max_length=128, unique=True, verbose_name="资产序列号")
    assets_name = models.CharField(max_length=64, unique=True, editable=True, verbose_name='资产名称')
    assets_status = models.SmallIntegerField(choices=assets_status, default=4, verbose_name='资产状态')
    assets_manufacturer = models.ForeignKey('ManufacturerAssets', null=True, blank=True, verbose_name='厂商',
                                            on_delete=models.SET_NULL)
    assets_business = models.ForeignKey('BusinessAssets', null=True, blank=True, on_delete=models.SET_NULL,
                                        verbose_name='所属业务线')
    assets_manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP地址')
    assets_tags = models.ManyToManyField('TagAssets', blank=True, verbose_name='资产标签')
    assets_admin = models.ForeignKey(User, blank=True, null=True, related_name='asset_admin',
                                     verbose_name='资产管理员', on_delete=models.PROTECT)
    assets_idc = models.ForeignKey('IDCAssets', related_name='assets_idc', on_delete=models.PROTECT, null=True,
                                   blank=True, verbose_name='所在机房')
    assets_cabinet = models.ForeignKey('CabinetAssets', related_name='assets_cabinet', null=True, blank=True,
                                       verbose_name='所在机柜', on_delete=models.PROTECT)
    assets_contract = models.ForeignKey('ContractAssets', null=True, blank=True, on_delete=models.SET_NULL,
                                        verbose_name='合同')
    assets_purchase_day = models.DateField(null=True, blank=True, verbose_name='购买日期')
    assets_expire_day = models.DateField(null=True, blank=True, verbose_name='过保日期')
    assets_price = models.CharField(max_length=100, null=True, blank=True, verbose_name='价格(RMB)')
    assets_approved = models.ForeignKey(User, null=True, blank=True, related_name='asset_approved',
                                        on_delete=models.SET_NULL, verbose_name='批准人')
    assets_c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准时间')
    assets_u_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    assets_memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return '<%s> %s' % (self.get_assets_type_display(), self.assets_name)

    class Meta:
        db_table = 'imu_assets'
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name
        ordering = ['-assets_c_time']


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
    type = models.SmallIntegerField(choices=server_type_choice, default=2, verbose_name="服务器类型")
    create_by = models.CharField(choices=server_create_by_choice, max_length=32, default='manual',
                                 verbose_name='添加方式')
    hostname = models.CharField(max_length=100, unique=True, null=True, editable=True, verbose_name='主机名')
    host_on = models.ForeignKey('self', related_name='host_on_server', blank=True, null=True,
                                verbose_name='宿主机', on_delete=models.CASCADE)
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='RAID卡类型')
    os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作系统类型')
    os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name='发行商')
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name='内核版本')

    def __str__(self):
        return '%s--%s--%s--<assets_num:%s>' % (self.assets.assets_name, self.get_type_display(),
                                                self.model, self.assets.assets_num)

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
    type = models.SmallIntegerField(choices=network_type_choice, default=1, verbose_name='设备类型')
    hostname = models.CharField(max_length=100, unique=True, editable=True, verbose_name='主机名')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='设备型号')
    port_num = models.IntegerField(blank=True, null=True, verbose_name='端口数')
    firmware = models.CharField(max_length=100, blank=True, null=True, verbose_name='固件版本')

    def __str__(self):
        return '%s--%s--%s--<assets_sn:%s>' % (self.assets.assets_name, self.get_type_display(),
                                               self.model, self.assets.assets_num)

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
    type = models.SmallIntegerField(choices=security_type_choice, default=9, verbose_name='产品类型')
    hostname = models.CharField(max_length=100, unique=True, editable=True, verbose_name='主机名')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='设备型号')
    firmware = models.CharField(max_length=100, blank=True, null=True, verbose_name='固件版本')

    def __str__(self):
        return self.assets.assets_name + "--" + self.get_type_display() + str(self.model) + "id:%s" \
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
    type = models.SmallIntegerField(choices=storage_type_choice, default=4, verbose_name='存储类型')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='设备型号')
    firmware = models.CharField(max_length=100, blank=True, null=True, verbose_name='固件版本')

    def __str__(self):
        return '%s--%s--%s<id:%s>' % (self.assets.assets_name, self.get_type_display(), str(self.model),
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
    assets = models.OneToOneField('Assets', related_name='soft_assets', on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=soft_type_choice, default=5, verbose_name='软件资产类型')
    license_num = models.IntegerField(default=1, verbose_name='授权数量')
    version = models.CharField(max_length=100, blank=True, null=True, help_text="例如：Cent 5.2.9-2kali1",
                               verbose_name='软件版本')

    def __str__(self):
        return '%s--%s--%s' % (self.assets.assets_name, self.get_type_display(), self.version)

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
    assets = models.OneToOneField('Assets', related_name='office_assets', on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=office_type_choice, default=7, verbose_name='办公设备类型')
    user = models.CharField(max_length=100, unique=True, editable=True, verbose_name='使用人')

    def __str__(self):
        return '%s--%s--%s' % (self.assets.assets_name, self.get_type_display(), self.user)

    class Meta:
        db_table = 'imu_office_assets'
        verbose_name = '办公设备资产表'
        verbose_name_plural = verbose_name


class ManufacturerAssets(models.Model):
    """厂商信息表"""

    name = models.CharField(max_length=100, unique=True, verbose_name='厂商名称')
    contacts = models.CharField(max_length=100, verbose_name='厂商联系人')
    phone = models.CharField(max_length=11, null=True, unique=True, verbose_name="联系人电话")
    email = models.EmailField(unique=True, null=True, verbose_name='联系邮箱')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return '%s--%s' % (self.name, self.contacts)

    class Meta:
        db_table = 'imu_manufacturer_assets'
        verbose_name = '厂商信息表'
        verbose_name_plural = verbose_name


class BusinessAssets(models.Model):
    """业务线"""

    name = models.CharField(max_length=100, unique=True, verbose_name='业务线名称')
    charge = models.ForeignKey(User, blank=True, verbose_name='业务负责人',
                               on_delete=models.PROTECT)
    department = models.CharField(max_length=100, blank=True, verbose_name='所属部门')

    def __str__(self):
        return self.name + self.department

    class Meta:
        db_table = 'imu_business_assets'
        verbose_name = '业务线资产表'
        verbose_name_plural = verbose_name


class TagAssets(models.Model):
    """资产标签表"""

    name = models.CharField(max_length=32, unique=True, verbose_name='标签名')
    c_day = models.DateField(auto_now_add=True, verbose_name='创建日期')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'imu_tag_assets'
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class IDCAssets(models.Model):
    """机房资产表"""

    name = models.CharField('机房名称', max_length=64, unique=True)
    address = models.CharField('机房地址', max_length=100, unique=True)
    contract = models.ForeignKey('ContractAssets', null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='机房合同')
    contact = models.CharField('机房联系人', max_length=32)
    telephone = models.CharField('支持电话', max_length=11, blank=True, null=True)
    memo = models.CharField('备注', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'imu_idc_assets'
        verbose_name = '机房表'
        verbose_name_plural = verbose_name


class CabinetAssets(models.Model):
    """机柜资产表"""

    idc = models.ForeignKey('IDCAssets', related_name='cabinet', on_delete=models.CASCADE)
    name = models.CharField('机柜名称', max_length=64, unique=True)
    U_num = models.CharField('机柜总U数', max_length=100, blank=True)
    used = models.CharField('已使用空间', max_length=100, blank=True)
    memo = models.CharField('备注', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'imu_cabinet_assets'
        verbose_name = '机柜表'
        verbose_name_plural = verbose_name


class ContractAssets(models.Model):
    """合同资产表"""

    sn = models.CharField('合同号', max_length=128, unique=True)
    name = models.CharField('合同名称', max_length=100)
    price = models.IntegerField('合同金额')
    detail = models.TextField('详细合同', blank=True, null=True)
    start_day = models.DateField('生效日期', blank=True, null=True)
    end_day = models.DateField('失效日期', blank=True, null=True)
    c_day = models.DateField('创建时间', auto_now_add=True)
    m_day = models.DateField('修改日期', auto_now=True)
    memo = models.TextField('备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'imu_contract_assets'
        verbose_name = "合同"
        verbose_name_plural = verbose_name


class NICAssets(models.Model):
    """网卡组件"""

    assets = models.ForeignKey('Assets', related_name='nic_assets', on_delete=models.CASCADE)  # 注意要用外键
    name = models.CharField('网卡名称', max_length=64, blank=True, null=True)
    model = models.CharField('网卡型号', max_length=128)
    mac = models.CharField('MAC地址', max_length=64)  # 虚拟机有可能会出现同样的mac地址
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
    net_mask = models.CharField('掩码', max_length=64, blank=True, null=True)
    binding = models.CharField('绑定地址', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s:  %s:  %s' % (self.assets.assets_name, self.model, self.mac)

    class Meta:
        db_table = 'imu_nic_assets'
        verbose_name = '网卡'
        verbose_name_plural = verbose_name
        unique_together = ('assets', 'model', 'mac')  # 资产、型号、MAC地址必须联合唯一，避免虚拟化中特殊情况发生错误。


class DiskAssets(models.Model):
    """硬盘设备"""

    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SAS', 'SAS'),
        ('IDE', 'IDE'),
        ('Fiber Channel', 'Fiber Channel'),
        ('UNKNOWN', 'UNKNOWN'),
    )

    assets = models.ForeignKey('Assets', related_name='disk_assets', on_delete=models.CASCADE)
    slot = models.CharField('所在插槽位', max_length=64, blank=True, null=True)
    sn = models.CharField('硬盘SN号', max_length=128)
    model = models.CharField('磁盘型号', max_length=128, blank=True, null=True)
    brand = models.CharField('磁盘制造商', max_length=128, blank=True, null=True)
    volume = models.FloatField('磁盘容量(GB)', blank=True, null=True)
    interface_type = models.CharField('接口类型', max_length=16, choices=disk_interface_type_choice,
                                      default='unknown')

    def __str__(self):
        return '%s:  %s:  %s:  %sGB' % (self.assets.assets_name, self.model, self.slot, self.volume)

    class Meta:
        db_table = 'imu_disk_assets'
        verbose_name = '硬盘'
        verbose_name_plural = verbose_name
        unique_together = ('assets', 'sn')  # 同一资产下的硬盘，根据SN不同必须唯一。


class RAMAssets(models.Model):
    """内存组件"""

    assets = models.ForeignKey('Assets', related_name='ram_assets', on_delete=models.CASCADE)
    sn = models.CharField('SN号', max_length=128, blank=True, null=True)
    model = models.CharField('内存型号', max_length=128, blank=True, null=True)
    brand = models.CharField('内存制造商', max_length=128, blank=True, null=True)
    slot = models.CharField('插槽', max_length=64)
    volume = models.IntegerField('内存大小(GB)', blank=True, null=True)

    def __str__(self):
        return '%s: %s: %s: %s' % (self.assets.assets_name, self.model, self.slot, self.volume)

    class Meta:
        db_table = 'imu_ram_assets'
        verbose_name = '内存'
        verbose_name_plural = verbose_name
        unique_together = ('assets', 'slot')  # 同一资产下的内存，根据插槽不同必须唯一。


class CPUAssets(models.Model):
    """CPU组件"""

    assets = models.OneToOneField('Assets', related_name='cpu_assets', on_delete=models.CASCADE)
    cpu_model = models.CharField('CPU型号', max_length=128, blank=True, null=True)
    cpu_count = models.PositiveSmallIntegerField('物理CPU个数', default=1)
    cpu_core_count = models.PositiveSmallIntegerField('CPU核数', default=1)

    def __str__(self):
        return self.assets.assets_name

    class Meta:
        db_table = 'imu_cpu_assets'
        verbose_name = 'CPU'
        verbose_name_plural = verbose_name


class DomainAssets(models.Model):
    """域名资产表"""

    name = models.CharField('域名名称', max_length=64, blank=True, null=True)
    address = models.URLField('域名地址', max_length=100, null=False)
    int_ip = models.GenericIPAddressField('对内IP地址', blank=True, null=True)
    out_ip = models.GenericIPAddressField('对外IP地址', blank=True, null=True)
    department = models.CharField('所属部门', max_length=64, blank=True, null=True)
    admin = models.ForeignKey(User, blank=True, related_name='domain_admin',
                              verbose_name='域名管理员', on_delete=models.PROTECT)

    class Meta:
        db_table = 'imu_domain_assets'
        verbose_name = '域名表'
        verbose_name_plural = verbose_name


class ProviderAssets(models.Model):
    """供应商信息表"""

    name = models.CharField('供应商名称', max_length=64, unique=True)
    contact = models.CharField('技术支持人员', max_length=32, blank=True, null=True)
    phone = models.CharField('支持电话', max_length=11, blank=True, null=True)
    email = models.EmailField('供应商邮箱', unique=True)
    memo = models.CharField('备注', max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'imu_provider_assets'
        verbose_name = '供应商表'
        verbose_name_plural = verbose_name


class CloudAssets(models.Model):
    """云平台资产表"""

    cloud_type_choice = (
        (0, '公有云'),
        (1, '私有云'),
    )
    type = models.SmallIntegerField('云类型', choices=cloud_type_choice, default=1)
    brand = models.CharField('云厂商', max_length=100, blank=True, null=True)
    admin = models.ForeignKey(User, blank=True, related_name='cloud_admin',
                              verbose_name='云平台管理员', on_delete=models.PROTECT)

    class Meta:
        db_table = 'imu_cloud_assets'
        verbose_name = '云平台资产表'
        verbose_name_plural = verbose_name


class OtherAssets(models.Model):
    """其他资产表"""

    name = models.CharField('资产名称', max_length=64, unique=True)
    sn = models.CharField('SN号', max_length=128, blank=True, null=True)
    admin = models.ForeignKey(User, blank=True, related_name='other_admin',
                              verbose_name='资产管理员', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'imu_other_assets'
        verbose_name = '其他资产表'
        verbose_name_plural = verbose_name


class EventLog(models.Model):
    """日志，关联的资源被删除时相关的日志不能被删除，应当被保留"""

    name = models.CharField('事件名称', max_length=128)
    event_type_choice = (
        (0, '其他'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '系统升级'),
        (7, '业务上线/变更/更新'),
    )

    assets = models.ForeignKey('Assets', blank=True, null=True, on_delete=models.SET_NULL)  # 日志不能随着资产删除而删除
    new_assets = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)
    type = models.SmallIntegerField('事件类型', choices=event_type_choice, default=0)
    component = models.CharField('事件子项', max_length=256, blank=True, null=True)
    detail = models.TextField('事件详情')
    date = models.DateTimeField('事件时间', auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name="事件执行人",
                             on_delete=models.SET_NULL)
    memo = models.TextField('备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'imu_log_assets'
        verbose_name = "事件记录"
        verbose_name_plural = verbose_name


class NewAssetApprovalZone(models.Model):
    """新资产待审批区域"""

    sn = models.CharField('资产SN号', max_length=128, unique=True)  # 此字段必填
    type_choice = (
        ('server', '服务器'),
        ('network', '网络设备'),
        ('storage', '存储设备'),
        ('security', '安全设备'),
        ('software', '软件资产'),
        ('office', '办公设备'),
        ('other', '其他设备'),
    )
    assets_type = models.CharField('资产类型', choices=type_choice, default='server', max_length=64, blank=True, null=True)
    manufacturer = models.CharField('生产厂商', max_length=64, blank=True, null=True)
    model = models.CharField('型号', max_length=128, blank=True, null=True)
    ram_volume = models.PositiveIntegerField('内存大小', blank=True, null=True)
    cpu_model = models.CharField('CPU型号', max_length=128, blank=True, null=True)
    cpu_count = models.PositiveSmallIntegerField('CPU物理数量', blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField('CPU核心数量', blank=True, null=True)
    os_distribution = models.CharField('发行商', max_length=64, blank=True, null=True)
    os_type = models.CharField('系统类型', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本号', max_length=64, blank=True, null=True)

    data = models.TextField('资产数据')  # 此字段必填

    c_time = models.DateTimeField('汇报日期', auto_now_add=True)
    u_time = models.DateTimeField('数据更新日期', auto_now=True)
    approved = models.BooleanField('是否批准', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        db_table = 'imu_NewAssetApprovalZone'
        verbose_name = '新上线待批准资产'
        verbose_name_plural = verbose_name
        ordering = ['-c_time']
