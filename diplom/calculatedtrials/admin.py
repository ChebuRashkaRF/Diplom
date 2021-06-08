from django.contrib import admin
from .models import *
from generaltables.models import *

class ReportInline(admin.TabularInline):
    model = Report
    exclude = ['report_experimental']
    extra = 0

class GraphInline(admin.TabularInline):
    model = Graph
    extra = 0

class SettlementFileInline(admin.TabularInline):
    model = SettlementFile
    extra = 0


@admin.register(Calculated)
class CalculatedAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in Calculated._meta.fields]
    list_filter = ('stand', 'data_calculated',)
    search_fields = ('aim_calculated', 'data_calculated',)
    ordering = ('data_calculated',)
    inlines = [ ReportInline, GraphInline, SettlementFileInline]
    exclude = ['slug_calculated']
    date_hierarchy = 'data_calculated'


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in Graph._meta.fields]
    list_filter = ('name_graph',)
    search_fields = ('name_graph',)
    ordering = ('name_graph',)

@admin.register(SettlementFile)
class SettlementFilesAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in SettlementFile._meta.fields]
    list_filter = ('name_settlementfile',)
    search_fields = ('name_settlementfile',)
    ordering = ('name_settlementfile',)
