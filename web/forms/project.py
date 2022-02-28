from django import forms
from web import models
from web.forms.bootstrap import BootStrapForm

from django.core.exceptions import ValidationError

class ProjectModelFrom(BootStrapForm,forms.ModelForm):
    # desc = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = models.Project
        fields = ['name','color','desc']
        widgets = {
            'desc':forms.Textarea(attrs={'描述':123})
        }
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request
    def clean_name(self):
        name = self.cleaned_data['name']
        #1.判断用户是否创建过项目
        # exists = models.Project.objects.filter(name = name).exists()
        exists = models.Project.objects.filter(name = name,creator = self.request.tracer.user).exists()
        if exists:
            raise ValidationError('项目已创建！')

        #2.是否有额度
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()
        if count >=  self.request.tracer.price_policy.project_num:
            raise ValidationError('项目数量超限，请购买')
        return name