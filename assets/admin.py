from django.contrib import admin
from assets import models


class NewAssetsAdmin(admin.ModelAdmin):
    list_display = ['type', 'sn', 'model', 'manufacturer', 'c_time', 'u_time']
    list_filter = ['type', 'manufacturer', 'c_time']
    search_fields = ('sn', )


class AssetsAdmin(admin.ModelAdmin):
    list_display = ['assets_type', 'assets_name', 'assets_status', 'assets_approved', 'assets_c_time',
                    'assets_u_time']


admin.site.register(models.Assets, AssetsAdmin)
admin.site.register(models.ServerAssets)
admin.site.register(models.NetworkAssets)
admin.site.register(models.SecurityAssets)
admin.site.register(models.StorageAssets)
admin.site.register(models.SoftAssets)
admin.site.register(models.OfficeAssets)
admin.site.register(models.ManufacturerAssets)
admin.site.register(models.BusinessAssets)
admin.site.register(models.TagAssets)
admin.site.register(models.IDCAssets)
admin.site.register(models.CabinetAssets)
admin.site.register(models.ContractAssets)
admin.site.register(models.NICAssets)
admin.site.register(models.DiskAssets)
admin.site.register(models.RAMAssets)
admin.site.register(models.CPUAssets)
admin.site.register(models.DomainAssets)
admin.site.register(models.ProviderAssets)
admin.site.register(models.CloudAssets)
admin.site.register(models.OtherAssets)
admin.site.register(models.EventLog)
admin.site.register(models.NewAssetApprovalZone, NewAssetsAdmin)



