from django.contrib import admin
from .models import *
from generaltables.models import *



# class ParameterObjectInline(admin.TabularInline):
#     model = ParameterObject
#     extra = 0

class ReportInline(admin.TabularInline):
    model = Report
    exclude = ['report_calculated']
    extra = 0



@admin.register(Experimental)
class Experimental(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in Experimental._meta.fields]
    list_filter = ('stand','data_experimental')
    search_fields = ('aim_experimental', 'data_experimental',)
    ordering = ('data_experimental',)
    inlines = [ReportInline]
    exclude = ['slug_experimental']
    date_hierarchy = 'data_experimental'
    # raw_id_fields = ('testobjects',)
