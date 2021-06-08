from django import forms
from .models import *

from django.forms import ModelForm
import os
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class TestObjectForm(ModelForm):

    class Meta:
        model = TestObject
        fields = '__all__'
        localized_fields = '__all__'



# class ParameterObjectForm(ModelForm):
#
#     class Meta:
#         model = ParameterObject
#         fields = '__all__'
#         localized_fields = '__all__'

class ParameterObjectForm(forms.Form):
    name_parametr_object = forms.CharField(
        max_length=100,
        label='Название параметра')
    value_parametr_object = forms.CharField(
        max_length=20,
        required=False,
        label='Значение параметра')
    measure_parametr_object = forms.CharField(
        max_length=10,
        required=False,
        label='Единица измерения')

    def clean_value_parametr_object(self):
        data = self.cleaned_data['value_parametr_object']
        s = '0123456789-^.x'
        for v in data:
            if v not in s:
                raise ValidationError(
                    _('В данном поле могут быть только цифры и знаки: " - ", " ^ ", " . ", " x "'),
                    code='error_number_parameter',
                )
        return data

    # def clean(self):
    #     cleaned_data = super(ParameterObjectForm, self).clean()
    #     name_parametr_object = cleaned_data.get("name_parametr_object")
    #     value_parametr_object = cleaned_data.get("value_parametr_object")
    #     measure_parametr_object = cleaned_data.get("measure_parametr_object")
    #     testobject = ParameterObject.objects.filter(name_parametr_object__iexact=name_parametr_object, value_parametr_object__iexact=value_parametr_object, measure_parametr_object__iexact=measure_parametr_object)
    #
    #     if testobject:
    #         raise ValidationError(
    #         _('Такой параметр уже существует.'),
    #         code='error_testobject',
    #         )

class TesterForm(ModelForm):

    class Meta:
        model = Tester
        fields = '__all__'
        localized_fields = '__all__'

    def clean(self):
        cleaned_data = super(TesterForm, self).clean()
        last_name = cleaned_data.get("last_name")
        first_name = cleaned_data.get("first_name")
        middle_name = cleaned_data.get("middle_name")
        department = cleaned_data.get("department")
        post = cleaned_data.get("post")
        tester = Tester.objects.filter(last_name__iexact=last_name,first_name__iexact=first_name, middle_name__iexact=middle_name, department__iexact=department, post__iexact=post)

        if tester:
            raise ValidationError(
            _('Такой испытатель уже существует.'),
            code='error_tester',
            )


# class TesterForm(forms.Form):
#
#     last_name = forms.CharField(
#         max_length=30,
#         label='Фамилия')
#     first_name = forms.CharField(
#         max_length=20,
#         label='Имя')
#     middle_name = forms.CharField(
#         max_length=30,
#         label='Отчество')
#     department = forms.CharField(
#         max_length=10,
#         label='Номер отдела')
#     post = forms.CharField(
#         max_length=70,
#         label='Должность')
#
#     def clean_department(self):
#         data = self.cleaned_data['department']
#         s = '0123456789'
#         for v in data:
#             if v not in s:
#                 raise ValidationError(
#                     _('В данном поле могут быть только цифры.'),
#                     code='error_number_department',
#                 )
#         return data
#     def clean(self):
#         cleaned_data = super(TesterForm, self).clean()
#         last_name = cleaned_data.get("last_name")
#         first_name = cleaned_data.get("first_name")
#         middle_name = cleaned_data.get("middle_name")
#         department = cleaned_data.get("department")
#         post = cleaned_data.get("post")
#         tester = Tester.objects.filter(last_name__iexact=last_name,first_name__iexact=first_name, middle_name__iexact=middle_name, department__iexact=department, post__iexact=post)
#
#         if tester:
#             raise ValidationError(
#             _('Такой испытатель уже существует.'),
#             code='error_tester',
#             )
