from django.contrib import admin
from .models import *

class ParameterObjectInline(admin.TabularInline):
    model = ParameterObject
    extra = 0


@admin.register(TestObject)
class TestObjectAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in TestObject._meta.fields]
    list_filter = ('title_object',)
    search_fields = ('title_object',)
    ordering = ('title_object',)
    inlines = [ParameterObjectInline]

@admin.register(ParameterObject)
class ParameterObjectAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in ParameterObject._meta.fields]
    list_filter = ('testobject',)
    search_fields = ('name_parametr_object',)
    ordering = ('testobject',)

@admin.register(Tester)
class TesterAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in Tester._meta.fields]
    list_filter = ('department',)
    search_fields = ('last_name', 'department',)
    ordering = ('last_name',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in Report._meta.fields]
    list_filter = ('name_report',)
    search_fields = ('name_report',)
    ordering = ('name_report',)
