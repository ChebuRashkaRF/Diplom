from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *
from generaltables.models import *
from stands.models import Stand

from .forms import *
from generaltables.forms import *
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.forms import BaseFormSet

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

# Таблица расчетных испытаний
@login_required
def calculated_stand(request, slug_stand):
    calculateds = Calculated.objects.prefetch_related('stand','testers','testobject','reports_calculated','graphs','settlementfiles').filter(stand__slug_stand__iexact=slug_stand)
    name_stand = Stand.objects.get(slug_stand=slug_stand).name_stand
    # print(name_stand)
    # calculated = Calculated.objects.all()[0]
    # print()
    # p = calculateds[0]
    # print(p)
    # print()
    # print(p.testobjects_object_calculated.get().title_object)
    # print(dir(p))
    # # print(stand.calculateds.all())
    return render(request, 'calculatedtrials/calculatedtrials-stand.html', context={'calculateds': calculateds, 'name_stand': name_stand})

# Конкретное расчетное испытания
@login_required
def calculatedtrial_detail(request, slug_stand, slug_calculated):
    calculated = Calculated.objects.prefetch_related('stand','testers','testobject','reports_calculated','graphs','settlementfiles').get(slug_calculated__iexact=slug_calculated, stand__slug_stand__iexact=slug_stand)

    return render(request, 'calculatedtrials/calculatedtrial-detail.html', context={'calculated': calculated})

# Таблица редактора
# @user_passes_test(lambda u: u.groups.filter(name='Redactor').exists())
@login_required
def calculated_redactor(request):
    calculateds = Calculated.objects.prefetch_related('stand','testers','testobject','reports_calculated','graphs','settlementfiles').all()
    return render(request, 'calculatedtrials/calculated-redactor.html', context={'calculateds': calculateds})

# Добавление Экспериментального испытания
class BaseReportCalculatedFormSet(BaseFormSet):
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

class BaseGraphFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        name_graphs = []
        for form in self.forms:
            if form.has_changed():
                name_graph = form.cleaned_data.get('name_graph')
                if name_graph in name_graphs:
                    err = _('Название файла должно быть уникальным.')
                    form.add_error(None, err)
                    # forms.ValidationError(_("Имя файла должно быть уникальным."))
                name_graphs.append(name_graph)

class BaseSettlementFileFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        name_settlementfiles = []
        for form in self.forms:
            if form.has_changed():
                name_settlementfile = form.cleaned_data.get('name_settlementfile')
                if name_settlementfile in name_settlementfiles:
                    err = _('Название файла должно быть уникальным.')
                    form.add_error(None, err)
                    # forms.ValidationError(_("Имя файла должно быть уникальным."))
                name_settlementfiles.append(name_settlementfile)

@login_required
def calculated_add(request):
    ReportCalculatedFormSet =  formset_factory(ReportCalculatedForm, formset=BaseReportCalculatedFormSet, extra=10)
    GraphFormSet =  formset_factory(GraphForm, formset=BaseGraphFormSet, extra=10)
    SettlementFileFormSet =  formset_factory(SettlementFileForm, formset=BaseSettlementFileFormSet, extra=10)
    if request.method == 'POST':
        form = CalculatedForm(request.POST)
        formset = ReportCalculatedFormSet(request.POST, request.FILES,)
        formset_graph = GraphFormSet(request.POST, request.FILES,)
        formset_file = SettlementFileFormSet(request.POST, request.FILES,)
        if form.is_valid() and formset.is_valid() and formset_graph.is_valid() and formset_file.is_valid():
            for forms in formset:
                if forms.has_changed():
                    name_report = forms.cleaned_data['name_report']
                    if Report.objects.filter(name_report=name_report).exists():
                        report_file = Report.objects.get(name_report=name_report)
                        if report_file.report_calculated != None:
                            errrep ='Такой файл уже существует.'
                            forms.add_error(None, errrep)
            if formset.is_valid():
                calculated = form.save()
                for forms in formset:
                    if forms.has_changed():
                        name_report = forms.cleaned_data['name_report']
                        if Report.objects.filter(name_report=name_report).exists():
                            report_file = Report.objects.filter(name_report=name_report)
                            if report_file.report_calculated == None:
                                Report.objects.filter(name_report=name_report).update(report_calculated = calculated)
                            else:
                                report = forms.cleaned_data['report']
                                obj_report = Report.objects.create(name_report=name_report, report=report, report_calculated=calculated)
                        else:
                            report = forms.cleaned_data['report']
                            obj_report = Report.objects.create(name_report=name_report, report=report, report_calculated=calculated)
                for forms in formset_graph:
                    if forms.has_changed():
                        name_graph = forms.cleaned_data['name_graph']
                        graph = forms.cleaned_data['graph']
                        obj_graph = Graph.objects.create(name_graph=name_graph, graph=graph, graph_calculated=calculated)
                for forms in formset_file:
                    if forms.has_changed():
                        name_settlementfile = forms.cleaned_data['name_settlementfile']
                        settlementfile = forms.cleaned_data['settlementfile']
                        obj_settlementfile = SettlementFile.objects.create(name_settlementfile=name_settlementfile, settlementfile=settlementfile, settlementfile_calculated=calculated)
                return render(request, 'calculatedtrials/calculated-add-success.html', context={'calculated': calculated})
    else:
        form = CalculatedForm()
        formset = ReportCalculatedFormSet()
        formset_graph = GraphFormSet()
        formset_file = SettlementFileFormSet()
    return render(request, 'calculatedtrials/calculated-add.html', {'form': form, 'formset': formset, 'formset_graph': formset_graph, 'formset_file': formset_file})

# Добваление объекта испытания
@login_required
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
def calculated_edit(request, slug_calculated):
    ReportCalculatedModelFormSet =  modelformset_factory(Report, exclude=('report_experimental', 'report_calculated'), can_delete=True, extra=0)
    GraphModelFormSet =  modelformset_factory(Graph, exclude=('graph_calculated',), can_delete=True, extra=0)
    SettlementFileModelFormFormSet =  modelformset_factory(SettlementFile, exclude=('settlementfile_calculated',), can_delete=True, extra=0)
    calculated = get_object_or_404(Calculated, slug_calculated=slug_calculated)
    ReportCalculatedFormSet =  formset_factory(ReportCalculatedForm, formset=BaseReportCalculatedFormSet, extra=5)
    GraphFormSet =  formset_factory(GraphForm, formset=BaseGraphFormSet, extra=5)
    SettlementFileFormSet =  formset_factory(SettlementFileForm, formset=BaseSettlementFileFormSet, extra=5)

    if request.method == 'POST':
        form = CalculatedForm(request.POST, instance=calculated)

        formset_model_r = ReportCalculatedModelFormSet(request.POST, request.FILES, queryset=Report.objects.filter(report_calculated__slug_calculated__iexact=slug_calculated), prefix='reportmodel')
        formset_r = ReportCalculatedFormSet(request.POST, request.FILES, prefix='report')

        formset_model_g = GraphModelFormSet(request.POST, request.FILES, queryset=Graph.objects.filter(graph_calculated__slug_calculated__iexact=slug_calculated), prefix='graphmodel')
        formset_g = GraphFormSet(request.POST, request.FILES, prefix='graph')

        formset_model_f = SettlementFileModelFormFormSet(request.POST, request.FILES, queryset=SettlementFile.objects.filter(settlementfile_calculated__slug_calculated__iexact=slug_calculated), prefix='filemodel')
        formset_f = SettlementFileFormSet(request.POST, request.FILES, prefix='file')
        if form.is_valid() and formset_r.is_valid() and formset_model_r.is_valid() and formset_g.is_valid() and formset_model_g.is_valid() and formset_f.is_valid() and formset_model_f.is_valid():
            for forms_model_r in formset_model_r:
                for forms in formset_r:
                    if forms.has_changed():
                        if forms.cleaned_data.get('name_report') == forms_model_r.cleaned_data.get('name_report'):
                            err = _('Название файла должно быть уникальным.')
                            forms.add_error(None, err)
                            forms_model_r.add_error(None, err)

            for forms in formset_r:
                name_report = forms.cleaned_data.get('name_report')
                if Report.objects.filter(name_report=name_report).exists():
                    report_file = Report.objects.get(name_report=name_report)
                    if report_file.report_calculated != None:
                        errrep ='Такой файл уже существует.'
                        forms.add_error(None, errrep)

            for forms_model_g in formset_model_g:
                for forms in formset_g:
                    if forms.has_changed():
                        if forms.cleaned_data.get('name_graph') == forms_model_g.cleaned_data.get('name_graph'):
                            err = _('Название файла должно быть уникальным.')
                            forms.add_error(None, err)
                            forms_model_g.add_error(None, err)

            for forms_model_f in formset_model_f:
                for forms in formset_f:
                    if forms.has_changed():
                        if forms.cleaned_data.get('name_settlementfile') == forms_model_f.cleaned_data.get('name_settlementfile'):
                            err = _('Название файла должно быть уникальным.')
                            forms.add_error(None, err)
                            forms_model_f.add_error(None, err)

            if formset_r.is_valid() and formset_model_r.is_valid() and formset_g.is_valid() and formset_model_g.is_valid() and formset_f.is_valid() and formset_model_f.is_valid():
                calculated = form.save()
                formset_model_r.save()
                formset_model_g.save()
                formset_model_f.save()
                for forms in formset_r:
                    if forms.has_changed():
                        name_report = forms.cleaned_data['name_report']
                        if Report.objects.filter(name_report=name_report).exists():
                            report_file = Report.objects.get(name_report=name_report)
                            if report_file.report_calculated == None:
                                Report.objects.filter(name_report=name_report).update(report_calculated = calculated)
                            else:
                                report = forms.cleaned_data['report']
                                obj_report = Report.objects.create(name_report=name_report, report=report, report_calculated=calculated)
                        else:
                            report = forms.cleaned_data['report']
                            obj_report = Report.objects.create(name_report=name_report, report=report, report_calculated=calculated)
                for forms in formset_g:
                    if forms.has_changed():
                        name_graph = forms.cleaned_data['name_graph']
                        graph = forms.cleaned_data['graph']
                        obj_graph = Graph.objects.create(name_graph=name_graph, graph=graph, graph_calculated=calculated)
                for forms in formset_f:
                    if forms.has_changed():
                        name_settlementfile = forms.cleaned_data['name_settlementfile']
                        settlementfile = forms.cleaned_data['settlementfile']
                        obj_settlementfile = SettlementFile.objects.create(name_settlementfile=name_settlementfile, settlementfile=settlementfile, settlementfile_calculated=calculated)
                return render(request, 'calculatedtrials/calculated-edit-success.html', context={'calculated': calculated})
    else:
        form = CalculatedForm(instance=calculated)

        formset_model_r = ReportCalculatedModelFormSet(queryset=Report.objects.filter(report_calculated__slug_calculated__iexact=slug_calculated), prefix='reportmodel')
        formset_r = ReportCalculatedFormSet(prefix='report')

        formset_model_g = GraphModelFormSet(queryset=Graph.objects.filter(graph_calculated__slug_calculated__iexact=slug_calculated), prefix='graphmodel')
        formset_g = GraphFormSet(prefix='graph')

        formset_model_f = SettlementFileModelFormFormSet(queryset=SettlementFile.objects.filter(settlementfile_calculated__slug_calculated__iexact=slug_calculated), prefix='filemodel')
        formset_f = SettlementFileFormSet(prefix='file')
    return render(request, 'calculatedtrials/calculated-edit.html', {'calculated': calculated, 'form': form, 'formset_model_r': formset_model_r, 'formset_r': formset_r, 'formset_model_g': formset_model_g, 'formset_g': formset_g, 'formset_model_f': formset_model_f, 'formset_f': formset_f })

# Редактирование объекта испытания
@login_required
def testobject_edit(request, slug_calculated):
    TestObjectFormSet =  modelformset_factory(TestObject, fields=('title_object',), can_delete=True, extra=0)
    calculated = get_object_or_404(Calculated, slug_calculated=slug_calculated)
    testobjects = TestObject.objects.filter(object_calculated__slug_calculated__iexact=slug_calculated)

    if request.method == 'POST':
        formset = TestObjectFormSet(request.POST, queryset=TestObject.objects.filter(object_calculated__slug_calculated__iexact=slug_calculated), prefix='testobject')
        if formset.is_valid():
            formset.save()
            return render(request, 'generaltables/testobject-edit-success.html', {'testobjects': testobjects })

    else:
        formset = TestObjectFormSet(queryset=TestObject.objects.filter(object_calculated__slug_calculated__iexact=slug_calculated), prefix='testobject')

    return render(request, 'generaltables/testobject-calculated-edit.html', {'calculated': calculated, 'formset': formset })

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
def parameter_edit(request, slug_calculated, testobjectid):
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
def tester_edit(request, slug_calculated):
    TesterFormSet =  modelformset_factory(Tester, fields=('__all__'), can_delete=True, extra=0)
    experimental = get_object_or_404(Calculated, slug_calculated=slug_calculated)
    testers = Tester.objects.filter(calculateds__slug_calculated__iexact=slug_calculated)

    if request.method == 'POST':
        formset = TesterFormSet(request.POST, queryset=Tester.objects.filter(calculateds__slug_calculated__iexact=slug_calculated), prefix='tester')
        if formset.is_valid():
            formset.save()
            return render(request, 'generaltables/tester-edit-success.html', {'testers': testers })

    else:
        formset = TesterFormSet(queryset=Tester.objects.filter(calculateds__slug_calculated__iexact=slug_calculated), prefix='tester')

    return render(request, 'generaltables/tester-edit.html', {'formset': formset })

# Информация про удаление испытания
@login_required
def calculated_info_delete(request, slug_calculated):
   calculated = get_object_or_404(Calculated, slug_calculated=slug_calculated)
   return render(request, 'calculatedtrials/calculated-info-delete.html', {'calculated':calculated })


# Удаление испытания
@login_required
def calculated_delete(request, slug_calculated):
   calculated = get_object_or_404(Calculated, slug_calculated=slug_calculated)
   objs = TestObject.objects.filter(object_calculated__slug_calculated__iexact=slug_calculated)
   for obj in objs:
       if not obj.objects_experimental.exists():
           obj.delete()
   testers = Tester.objects.filter(calculateds__slug_calculated__iexact=slug_calculated)
   for tester in testers:
       if tester.calculateds.count() == 1 and not tester.experimentals_tester.exists():
           tester.delete()
   reports = Report.objects.filter(report_calculated__slug_calculated__iexact=slug_calculated)
   for report in reports:
       if not report.report_experimental.exists():
           report.delete()
   calculated.delete()
   return HttpResponseRedirect(reverse('stands:calculated-redactor'))
