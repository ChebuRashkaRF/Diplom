from django.urls import path, include
from .views import *

urlpatterns = [
    # Редактор испытаний
    path('experimental-redactor/', experimental_redactor, name = 'experimental-redactor'),

    # Добавление
    path('experimental-redactor/experimental-add/', experimental_add, name = 'experimental-add'),
    path('experimental-redactor/testobject-add', testobject_add, name = 'testobject-add'),
    path('experimental-redactor/tester-add', tester_add, name = 'tester-add'),

    # Изменение
    path('experimental-redactor/<str:slug_experimental>/experimental-edit', experimental_edit, name = 'experimental-edit'),
    path('experimental-redactor/<str:slug_experimental>/experimental-edit/testobject-edit', testobject_edit, name = 'testobject-edit'),
    path('experimental-redactor/<str:slug_experimental>/experimental-edit/testobject-edit/<int:testobjectid>/parameter-edit', parameter_edit, name = 'parameter-edit'),
    path('experimental-redactor/<str:slug_experimental>/experimental-edit/tester-edit/', tester_edit, name = 'tester-edit'),

    # Удаление
    path('experimental-redactor/<str:slug_experimental>/experimental-info-delete/', experimental_info_delete, name = 'experimental-info-delete'),
    path('experimental-redactor/<str:slug_experimental>/experimental-info-delete/experimental-delete', experimental_delete, name = 'experimental-delete'),




    # Пользовательксий вид
    path('<str:slug_stand>/', experimental_stand, name = 'experimental-stand'),
    path('<str:slug_stand>/<str:slug_experimental>/', experimental_detail, name = 'experimental-detail'),

]
