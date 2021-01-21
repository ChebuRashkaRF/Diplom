from django import forms
from .models import *
from generaltables.models import *
from django.forms import ModelForm
import os
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class CalculatedForm(ModelForm):

    class Meta:
        model = Calculated
        exclude  = ['slug_calculated']
        localized_fields = '__all__'

class GraphForm(ModelForm):

    class Meta:
        model = Graph
        exclude  = ['graph_calculated']
        localized_fields = '__all__'

class SettlementFileForm(ModelForm):

    class Meta:
        model = SettlementFile
        exclude  = ['settlementfile_calculated']
        localized_fields = '__all__'

        # widgets = {
        #     'aim_experimental': forms.TextInput(attrs={'class': 'form-control'}),
        #
        # }

# class ReportForm(ModelForm):
#
#     class Meta:
#         model = Report
#         exclude  = ['report_calculated']
#         localized_fields = '__all__'
#
#         # widgets = {
#         #     'report_experimental': forms.Select(attrs={'type': 'hidden'}),
#         #
#         # }

class ReportCalculatedForm(forms.Form):
    name_report = forms.CharField(
        max_length=150,
        label='Название файла')
    report = forms.FileField(
        max_length=150,
        help_text="Разрешенные типы файлов: 'rar', 'pdf', 'doc', 'txt' и т.д.",
        label='Файл')

    def clean_report(self):
        data = self.cleaned_data['report']
        ext = os.path.splitext(data.name)[1]
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
        if ext.lower() in valid_extensions:
            raise ValidationError(
            _('Неподдерживаемое расширение файла.'),
            code='error_file',
            )
        return data

    # def clean_name_report(self):
    #     data = self.cleaned_data['name_report']
    #     report = Report.objects.filter(name_report__iexact=data)
    #     if report:
    #         raise ValidationError(
    #         _('Такое имя файла уже существует.'),
    #         code='error_name_report',
    #         )
    #     return data
    #
