from django.urls import path, include
from .views import *

urlpatterns = [
    # Редактор испытаний
    path('calculated-redactor/', calculated_redactor, name = 'calculated-redactor'),

    # Добавление
    path('calculated-redactor/calculated-add/', calculated_add, name = 'calculated-add'),
    path('calculated-redactor/testobject-add', testobject_add, name = 'testobject-calculated-add'),
    path('calculated-redactor/tester-add', tester_add, name = 'tester-calculated-add'),

    # Изменение
    path('calculated-redactor/<str:slug_calculated>/calculated-edit', calculated_edit, name = 'calculated-edit'),
    path('calculated-redactor/<str:slug_calculated>/calculated-edit/testobject-edit', testobject_edit, name = 'testobject-calculated-edit'),
    path('calculated-redactor/<str:slug_calculated>/calculated-edit/testobject-edit/<int:testobjectid>/parameter-edit', parameter_edit, name = 'parameter-calculated-edit'),
    path('calculated-redactor/<str:slug_calculated>/calculated-edit/tester-edit/', tester_edit, name = 'tester-calculated-edit'),

    # Удаление
    path('calculated-redactor/<str:slug_calculated>/calculated-info-delete/', calculated_info_delete, name = 'calculated-info-delete'),
    path('calculated-redactor/<str:slug_calculated>/calculated-info-delete/calculated-delete', calculated_delete, name = 'calculated-delete'),


    # Пользовательксий вид
    path('<str:slug_stand>/', calculated_stand, name = 'calculated-stand'),
    path('<str:slug_stand>/<str:slug_calculated>/', calculatedtrial_detail, name = 'calculatedtrial-detail'),

]
