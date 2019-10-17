from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from assets import models
from assets import assets_handler

# Create your views here.
@csrf_exempt
def report(request):
    if request.method == "POST":
        assets_data = request.POST.get('assets_data')
        print(assets_data)
        data = json.loads(assets_data)
        # 判断data是否为空
        if not data:
            return HttpResponse("提交的数据为空！")
        if not issubclass(dict, type(data)):
            return HttpResponse("提交的数据必须是字典格式！")
        # 判断提交的数据是否有唯一键：sn
        sn = data.get('sn', None)
        if sn:
            # 判断是否为线上资产中存在的资产
            assets_obj = models.Assets.objects.filter(sn=sn)
            if assets_obj:
                # 更新线上资产信息
                update_assets = assets_handler.UpdateAsset(request, assets_obj[0], data)
                return HttpResponse("资产已更新！")
            else:
                # 进入待审批区域
                obj = assets_handler.NewAssets(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse("提交的数据中未包含SN，请校验数据！")
    return HttpResponse("怎么就200了！")

