from django.shortcuts import render

from .models import *

from django.contrib.auth.decorators import login_required

@login_required
def testobjects_list(request):
    testobjects = TestObject.objects.prefetch_related('parameters_object', 'object_calculated', 'objects_experimental').all()
    # name_stand = calculateds[0].stand.name_stand
    # print(name_stand)
    # calculated = Calculated.objects.all()[0]
    # p = testobjects[1]
    # print()
    # print(p.object_calculated)
    # print()
    # print(p.testobjects_object_calculated.get().title_object)
    # print(dir(p))
    # # print(stand.calculateds.all())
    return render(request, 'generaltables/testobjects-list.html', context={'testobjects': testobjects})
