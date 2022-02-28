from web.forms.project import ProjectModelFrom
from django.shortcuts import  render
from django.http import JsonResponse


def project_list(request):
    if request.method == 'GET':
        form = ProjectModelFrom(request)
        return render(request,'project_list.html',{'form':form})
    form = ProjectModelFrom(request,data=request.POST)
    if form.is_valid():
        form.instance.creator = request.tracer.user
        form.save()
    return JsonResponse({'status':False,'error':form.errors})