from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *
from stands.models import Stand
from generaltables.models import *

from .forms import *
from generaltables.forms import *
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.forms import BaseFormSet

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required


# Таблица экспериментальных испытаний
@login_required
def experimental_stand(request, slug_stand):
    experimentals = Experimental.objects.prefetch_related('stand','testers','testobjects','reports_experimental').filter(stand__slug_stand__iexact=slug_stand)
    name_stand = Stand.objects.get(slug_stand=slug_stand).name_stand
    return render(request, 'trials/experimental-stand.html', context={'experimentals': experimentals, 'name_stand': name_stand})


# Конкретное экспериментальное испытания
@login_required
def experimental_detail(request, slug_stand, slug_experimental):
    experimental = Experimental.objects.prefetch_related('stand','testers','testobjects','reports_experimental').get(slug_experimental__iexact=slug_experimental, stand__slug_stand__iexact=slug_stand)
    # name_stand = Stand.objects.get(slug_stand=slug_stand).name_stand

    return render(request, 'trials/experimental-detail.html', context={'experimental': experimental})


# Таблица редактора
@login_required
def experimental_redactor(request):
    experimentals = Experimental.objects.prefetch_related('stand','testers','testobjects','reports_experimental').all()
    return render(request, 'trials/experimental-redactor.html', context={'experimentals': experimentals})

# Добавление Экспериментального испытания
class BaseReportExperimentalFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        name_reports = []
        for form in self.forms:
            if form.has_changed():
                name_report = form.cleaned_data.get('name_report')
                if name_report in name_reports:
                    err = _('Название файла должно быть уникальным.')
                    form.add_error(None, err)
                    # forms.ValidationError(_("Имя файла должно быть уникальным."))
                name_reports.append(name_report)

@login_required
def experimental_add(request):
    ReportExperimentalFormSet =  formset_factory(ReportExperimentalForm, formset=BaseReportExperimentalFormSet, extra=10)
    if request.method == 'POST':
        form = ExperimentalForm(request.POST)
        formset = ReportExperimentalFormSet(request.POST, request.FILES,)
        if form.is_valid() and formset.is_valid():
            for forms in formset:
                if forms.has_changed():
                    name_report = forms.cleaned_data['name_report']
                    if Report.objects.filter(name_report=name_report).exists():
                        report_file = Report.objects.get(name_report=name_report)
                        if report_file.report_experimental != None:
                            errrep ='Такой файл уже существует.'
                            forms.add_error(None, errrep)
            if formset.is_valid():
                experimental = form.save()
                for forms in formset:
                    if forms.has_changed():
                        name_report = forms.cleaned_data['name_report']
                        if Report.objects.filter(name_report=name_report).exists():
                            report_file = Report.objects.filter(name_report=name_report)
                            if report_file.report_experimental == None:
                                Report.objects.filter(name_report=name_report).update(report_experimental = experimental)
                            else:
                                report = forms.cleaned_data['report']
                                obj_report = Report.objects.create(name_report=name_report, report=report, report_experimental=experimental)
                        else:
                            report = forms.cleaned_data['report']
                            obj_report = Report.objects.create(name_report=name_report, report=report, report_experimental=experimental)
                return render(request, 'trials/experimental-add-success.html', context={'experimental': experimental})

        #     # for forms in formset:
        #     #     forms.fields['report_experimental'] = form.fields['aim_experimental']
        #     #     print(forms.fields['report_experimental'])
        #     a = form.save()
        #     print()
        #     print(a)
        #     print()
        #     print(a.id)
        #     for forms in formset:
        #         forms.fields['report_experimental'] = 'a'
        #     if formset.is_valid():
        #         for form in formset:
        #             print(form.cleaned_data)
        #             print(form.has_changed())
        #         print()
        #         print('hi formset')
        #         print()
        #         pass
        #     # return HttpResponseRedirect(reverse('stands:stands-list'))
        #     else:
        #         a.delete()
        #         print()
        #         print('hi no formset')
        #         print()
        #
        #         print()
        #         print()
        # else:
        #     print()
        #     print('hi no form')
        #     print()
    else:
        form = ExperimentalForm()
        formset = ReportExperimentalFormSet()
    return render(request, 'trials/experimental-add.html', {'form': form, 'formset': formset})


# Добваление объекта испытания
class BaseParameterObjectFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        testobjects = []
        name_parametr_objects = []
        for form in self.forms:
            if form.has_changed():
                name_parametr_object = form.cleaned_data.get('name_parametr_object')
                value_parametr_object = form.cleaned_data.get('value_parametr_object')
                measure_parametr_object = form.cleaned_data.get('measure_parametr_object')
                parameter_object = [name_parametr_object, value_parametr_object, measure_parametr_object]
                if parameter_object in testobjects:
                    err1 = _('Параметры объекта испытания должны быть уникальны.')
                    form.add_error(None, err1)
                    # raise forms.ValidationError(_("Параметры объекта испытания должны быть уникальны."))
                if name_parametr_object in name_parametr_objects:
                    err2 = _('Параметры объекта испытания должны быть уникальны.')
                    form.add_error(None, err2)
                    # raise forms.ValidationError(_("Параметры объекта испытания должны быть уникальными."))
                testobjects.append(parameter_object)
                name_parametr_objects.append(name_parametr_object)

@login_required
def testobject_add(request):
    ParameterObjectFormSet =  formset_factory(ParameterObjectForm, formset=BaseParameterObjectFormSet, validate_min=True, min_num=1, extra=9)
    if request.method == 'POST':
        form = TestObjectForm(request.POST)
        formset = ParameterObjectFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            testobject = form.save()
            for forms in formset:
                if forms.has_changed():
                    name_parametr_object = forms.cleaned_data['name_parametr_object']
                    value_parametr_object = forms.cleaned_data['value_parametr_object']
                    measure_parametr_object = forms.cleaned_data['measure_parametr_object']
                    obj_parameter = ParameterObject.objects.create(testobject=testobject, name_parametr_object=name_parametr_object, value_parametr_object=value_parametr_object, measure_parametr_object=measure_parametr_object)
            return render(request, 'generaltables/testobject-add-success.html', context={'testobject': testobject})

    else:
        form = TestObjectForm()
        formset = ParameterObjectFormSet()
    return render(request, 'generaltables/testobject-add.html', {'form': form, 'formset': formset})


# Добавление испытателя
class BaseTesterFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        tester = []
        person = []
        for form in self.forms:
            if form.has_changed():
                last_name = form.cleaned_data.get('last_name')
                first_name = form.cleaned_data.get('first_name')
                middle_name = form.cleaned_data.get('middle_name')
                department = form.cleaned_data.get('department')
                post = form.cleaned_data.get('post')
                person = [last_name, first_name, middle_name, department, post]
                if person in tester:
                    err = _('Испытатель должен быть уникальным.')
                    form.add_error(None, err)
                    # raise forms.ValidationError(_("Испытатель должен быть уникальным."))
                tester.append(person)

@login_required
def tester_add(request):
    TesterFormSet =  formset_factory(TesterForm, formset=BaseTesterFormSet, validate_min=True, min_num=1, extra=9)
    if request.method == 'POST':
        formset = TesterFormSet(request.POST)
        if formset.is_valid():
            testers = []
            for forms in formset:
                if forms.has_changed():
                    last_name = forms.cleaned_data['last_name']
                    first_name = forms.cleaned_data['first_name']
                    middle_name = forms.cleaned_data['middle_name']
                    department = forms.cleaned_data['department']
                    post = forms.cleaned_data['post']
                    tester = Tester.objects.create(last_name=last_name, first_name=first_name, middle_name=middle_name, department=department, post=post)
                    testers.append(tester)
            return render(request, 'generaltables/tester-add-success.html', context={'testers': testers,})
    else:
        formset = TesterFormSet()
    return render(request, 'generaltables/tester-add.html', context={'formset': formset,})


# редактирование испытания
@login_required
def experimental_edit(request, slug_experimental):
    # i = 1
    ReportExperimentalModelFormSet =  modelformset_factory(Report, exclude=('report_experimental', 'report_calculated'), can_delete=True, extra=0)
    experimental = get_object_or_404(Experimental, slug_experimental=slug_experimental)
    ReportExperimentalFormSet =  formset_factory(ReportExperimentalForm, formset=BaseReportExperimentalFormSet, extra=5)
    if request.method == 'POST':
        form = ExperimentalForm(request.POST, instance=experimental)
        formset_model = ReportExperimentalModelFormSet(request.POST, request.FILES, queryset=Report.objects.filter(report_experimental__slug_experimental__iexact=slug_experimental), prefix='reportmodel')
        formset = ReportExperimentalFormSet(request.POST, request.FILES, prefix='report')
        # for forms_model in formset_model:
        #     for forms in formset:
        #         if forms.has_changed():
        #             if forms.cleaned_data.get('name_report') == forms_model.cleaned_data.get('name_report'):
        #                 ar = _('привет')
        #                 forms.add_error(None, ar)
        if form.is_valid() and formset.is_valid() and formset_model.is_valid():
            for forms_model in formset_model:
                for forms in formset:
                    if forms.has_changed():
                        if forms.cleaned_data.get('name_report') == forms_model.cleaned_data.get('name_report'):
                            err = _('Название файла должно быть уникальным.')
                            forms.add_error(None, err)
                            forms_model.add_error(None, err)
            for forms in formset:
                name_report = forms.cleaned_data.get('name_report')
                if Report.objects.filter(name_report=name_report).exists():
                    report_file = Report.objects.get(name_report=name_report)
                    if report_file.report_experimental != None:
                        errrep ='Такой файл уже существует.'
                        forms.add_error(None, errrep)

            if formset.is_valid() and formset_model.is_valid():
                experimental = form.save()
                formset_model.save()
                for forms in formset:
                #     # if i:
                #     #     ar = _('привет')
                #     #     forms.add_error(None, ar)
                #         # raise forms.ValidationError(_("ап."))
                    if forms.has_changed():
                        name_report = forms.cleaned_data['name_report']
                        if Report.objects.filter(name_report=name_report).exists():
                            report_file = Report.objects.get(name_report=name_report)
                            if report_file.report_experimental == None:
                                Report.objects.filter(name_report=name_report).update(report_experimental = experimental)
                            else:
                                report = forms.cleaned_data['report']
                                obj_report = Report.objects.create(name_report=name_report, report=report, report_experimental=experimental)
                        else:
                            report = forms.cleaned_data['report']
                            obj_report = Report.objects.create(name_report=name_report, report=report, report_experimental=experimental)
                return render(request, 'trials/experimental-edit-success.html', context={'experimental': experimental})
    else:
        form = ExperimentalForm(instance=experimental)
        formset_model = ReportExperimentalModelFormSet(queryset=Report.objects.filter(report_experimental__slug_experimental__iexact=slug_experimental), prefix='reportmodel')
        formset = ReportExperimentalFormSet(prefix='report')
    return render(request, 'trials/experimental-edit.html', {'experimental': experimental,'form': form, 'formset_model': formset_model, 'formset': formset })


# Редактирование объекта испытания
@login_required
def testobject_edit(request, slug_experimental):
    TestObjectFormSet =  modelformset_factory(TestObject, fields=('title_object',), can_delete=True, extra=0)
    experimental = get_object_or_404(Experimental, slug_experimental=slug_experimental)
    testobjects = TestObject.objects.filter(objects_experimental__slug_experimental__iexact=slug_experimental)

    if request.method == 'POST':
        formset = TestObjectFormSet(request.POST, queryset=TestObject.objects.filter(objects_experimental__slug_experimental__iexact=slug_experimental), prefix='testobject')
        if formset.is_valid():
            formset.save()
            return render(request, 'generaltables/testobject-edit-success.html', {'testobjects': testobjects })

    else:
        formset = TestObjectFormSet(queryset=TestObject.objects.filter(objects_experimental__slug_experimental__iexact=slug_experimental), prefix='testobject')

    return render(request, 'generaltables/testobject-edit.html', {'experimental': experimental, 'formset': formset })


# Редактирование параметров
class BaseParameterObjectFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        name_parametr_objects = []
        for form in self.forms:
            if form.has_changed():
                name_parametr_object = form.cleaned_data.get('name_parametr_object')
                if name_parametr_object in name_parametr_objects:
                    err = _('Параметры объекта испытания должны быть уникальны.')
                    form.add_error(None, err)
                    # forms.ValidationError(_("Имя файла должно быть уникальным."))
                name_parametr_objects.append(name_parametr_object)

@login_required
def parameter_edit(request, slug_experimental, testobjectid):
    ParameterObjectModelFormSet =  modelformset_factory(ParameterObject, exclude=('testobject',), can_delete=True, extra=0)
    ParameterObjectFormSet =  formset_factory(ParameterObjectForm, formset=BaseParameterObjectFormSet, extra=5)
    if request.method == 'POST':
        formset_model = ParameterObjectModelFormSet(request.POST, queryset=ParameterObject.objects.filter(testobject=testobjectid), prefix='paranetermodel')
        formset = ParameterObjectFormSet(request.POST, prefix='paraneter')
        if formset.is_valid() and formset_model.is_valid():
            for forms_model in formset_model:
                for forms in formset:
                    if forms.has_changed():
                        if forms.cleaned_data.get('name_parametr_object') == forms_model.cleaned_data.get('name_parametr_object'):
                            err = _('Параметры объекта испытания должны быть уникальны.')
                            forms.add_error(None, err)
                            forms_model.add_error(None, err)
            if formset.is_valid() and formset_model.is_valid():
                formset_model.save()
                testobject = TestObject.objects.get(pk=testobjectid)
                for forms in formset:
                    if forms.has_changed():
                        name_parametr_object = forms.cleaned_data['name_parametr_object']
                        value_parametr_object = forms.cleaned_data['value_parametr_object']
                        measure_parametr_object = forms.cleaned_data['measure_parametr_object']
                        obj_parameter = ParameterObject.objects.create(testobject=testobject, name_parametr_object=name_parametr_object, value_parametr_object=value_parametr_object,measure_parametr_object=measure_parametr_object)
                return render(request, 'generaltables/parameter-edit-success.html', context={'testobject': testobject, 'slug_experimental': slug_experimental})
    else:
        formset_model = ParameterObjectModelFormSet(queryset=ParameterObject.objects.filter(testobject=testobjectid), prefix='paranetermodel')
        formset = ParameterObjectFormSet(prefix='paraneter')
    return render(request, 'generaltables/parameter-edit.html', { 'formset_model': formset_model, 'formset': formset })


# Редактирование испытателей
@login_required
def tester_edit(request, slug_experimental):
    TesterFormSet =  modelformset_factory(Tester, fields=('__all__'), can_delete=True, extra=0)
    experimental = get_object_or_404(Experimental, slug_experimental=slug_experimental)
    testers = Tester.objects.filter(experimentals_tester__slug_experimental__iexact=slug_experimental)

    if request.method == 'POST':
        formset = TesterFormSet(request.POST, queryset=Tester.objects.filter(experimentals_tester__slug_experimental__iexact=slug_experimental), prefix='tester')
        if formset.is_valid():
            formset.save()
            return render(request, 'generaltables/tester-edit-success.html', {'testers': testers })

    else:
        formset = TesterFormSet(queryset=Tester.objects.filter(experimentals_tester__slug_experimental__iexact=slug_experimental), prefix='tester')

    return render(request, 'generaltables/tester-edit.html', {'formset': formset })

# Информация про удаление испытания
@login_required
def experimental_info_delete(request, slug_experimental):
    experimental = get_object_or_404(Experimental, slug_experimental=slug_experimental)
    return render(request, 'trials/experimental-info-delete.html', {'experimental': experimental })


# Удаление испытания
@login_required
def experimental_delete(request, slug_experimental):
    experimental = get_object_or_404(Experimental, slug_experimental=slug_experimental)
    objs = TestObject.objects.filter(objects_experimental__slug_experimental__iexact=slug_experimental)
    for obj in objs:
        if obj.objects_experimental.count() == 1 and not obj.object_calculated.exists():
            obj.delete()
    testers = Tester.objects.filter(experimentals_tester__slug_experimental__iexact=slug_experimental)
    for tester in testers:
        if tester.experimentals_tester.count() == 1 and not tester.calculateds.exists():
            tester.delete()
    reports = Report.objects.filter(report_experimental__slug_experimental__iexact=slug_experimental)
    for report in reports:
        if not report.report_calculated.exists():
            report.delete()
    experimental.delete()
    return HttpResponseRedirect(reverse('stands:experimental-redactor'))
