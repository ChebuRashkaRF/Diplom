from django.shortcuts import render

from .models import Stand, DocumentStand

from django.db.models import Q

from django.contrib.auth.decorators import login_required

@login_required
def stands_list(request):

    stands = Stand.objects.all()

    # Получаем изображения
    list_img =[]
    for stand in stands:
        imgs = stand.documents.filter(
            Q(document__endswith='.jpg') |
            Q(document__endswith='.png') |
            Q(document__endswith='.gif') |
            Q(document__endswith='.jpeg') |
            Q(document__endswith='.svg')
        )
        list_img.append(imgs)

    # Получаем файлы
    list_file =[]
    for stand in stands:
        files = stand.documents.exclude(
            Q(document__endswith='.jpg') |
            Q(document__endswith='.png') |
            Q(document__endswith='.gif') |
            Q(document__endswith='.jpeg') |
            Q(document__endswith='.svg')
        )
        list_file.append(files)

    return render(request, 'stands/home_stand.html', context={'stands': stands, 'imgs_kvant': list_img[0], 'imgs_luch': list_img[1], 'files_kvant': list_file[0], 'files_luch': list_file[1]})
