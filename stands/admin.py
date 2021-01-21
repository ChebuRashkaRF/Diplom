from django.contrib import admin
from .models import *
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('content_type',)
    search_fields = ['user__username',]
    date_hierarchy = 'action_time'
admin.site.register(LogEntry, LogEntryAdmin)


class DocumentStandInline(admin.TabularInline):
    model = DocumentStand
    extra = 0

class ParameterStandInline(admin.TabularInline):
    model = ParameterStand
    extra = 0


@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in Stand._meta.fields]
    list_filter = ('name_stand',)
    search_fields = ('name_stand',)
    ordering = ('name_stand',)
    inlines = [DocumentStandInline, ParameterStandInline]
    exclude = ['slug_stand']

    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    # date_hierarchy = 'publish'


    # class Meta:
    #     model = Stand

@admin.register(DocumentStand)
class DocumentStandAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in DocumentStand._meta.fields]
    list_filter = ('stand',)
    search_fields = ('name_document',)
    ordering = ('stand',)

@admin.register(ParameterStand)
class ParameterStandAdmin(admin.ModelAdmin):
    # list_display = ('name_stand', 'slug')
    list_display = [field.name for field in ParameterStand._meta.fields]
    list_filter = ('stand',)
    # search_fields = ('name_parametr_stand',)
    ordering = ('stand',)
