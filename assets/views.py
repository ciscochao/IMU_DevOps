from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def report(request):
    if request.method == "POST":
        assets_data = request.POST.get('assets_data')
        print(assets_data)
        return HttpResponse("成功接收到数据!")
