from django.contrib import admin
from assets import models
from assets import assets_handler


class NewAssetsAdmin(admin.ModelAdmin):
    list_display = ['assets_type', 'sn', 'model', 'manufacturer', 'c_time', 'u_time']
    list_filter = ['assets_type', 'manufacturer', 'c_time']
    search_fields = ('sn', )

    actions = ['approve_selected_new_assets']

    def approve_selected_new_assets(self, request, queryset):
        # 获取复选框选中的资产
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        success_online_number = 0
        for assets_id in selected:
            obj = assets_handler.ApproveAssets(request, assets_id)
            ret = obj.assets_online()
            if ret:
                success_online_number += 1

        # 顶部绿色提醒
        self.message_user(request, "成功批准 %s 条新资产上线！" % success_online_number)
    approve_selected_new_assets.short_description = "批准选已选新资产"


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



