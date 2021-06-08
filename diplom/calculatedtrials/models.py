from django.db import models
from django.urls import reverse

from django.utils.text import slugify
from time import time

import os
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# Проверка расширения для документов
def validate_report_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
    if ext.lower() in valid_extensions:
        raise ValidationError(
        _('Неподдерживаемое расширение файла.'),
        code='error_file',
        )

# Генерируем slug
def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug.upper() + "-" + str(int(time()))

# меняем имя файла и указываем путь
def content_graph_name(instance, filename):
    extension_graph = instance.graph.name.rsplit('.', 1)[1].lower()
    new_name_graph = instance.graph_calculated.stand.name_stand + '/graph/' + str(instance.graph_calculated.data_calculated) + '/' + instance.name_graph + '.' + extension_graph
    instance.graph.name = new_name_graph
    return "calculatedtrials/{subfolder}".format(subfolder=instance.graph.name)

# меняем имя файла и указываем путь
def content_settlementfile_name(instance, filename):
    extension_settlementfile = instance.settlementfile.name.rsplit('.', 1)[1].lower()
    new_name_settlementfile = instance.settlementfile_calculated.stand.name_stand + '/settlementfiles/' + str(instance.settlementfile_calculated.data_calculated) + '/' + instance.name_settlementfile + '.' + extension_settlementfile
    instance.settlementfile.name = new_name_settlementfile
    return "calculatedtrials/{subfolder}".format(subfolder=instance.settlementfile.name)


class Calculated(models.Model):
    aim_calculated = models.CharField(
        max_length=250,
        verbose_name='Цель расчетного испытания',
        db_index=True)
    slug_calculated = models.SlugField(
        max_length=250,
        blank=True,
        unique=True)
    stand = models.ForeignKey(
        'stands.Stand',
        on_delete = models.CASCADE,
        related_name='calculateds',
        verbose_name = 'Стенд')
    testobject = models.ForeignKey(
        'generaltables.TestObject',
        on_delete = models.CASCADE,
        related_name='object_calculated',
        verbose_name = 'Объект испытания')
    testers = models.ManyToManyField(
        'generaltables.Tester',
        related_name='calculateds',
        verbose_name = 'Испытатель')
    data_calculated = models.DateField(
        verbose_name='Дата расчетного испытания',
        db_index=True,
        help_text="Введите дату по данному формату: <em>DD.MM.YYYY</em>")

    def get_detail_url(self):
        return reverse('stands:calculatedtrial-detail', kwargs={'slug_stand': self.stand.slug_stand, 'slug_calculated': self.slug_calculated})

    def get_edit_url(self):
        return reverse('stands:calculated-edit', kwargs={'slug_calculated': self.slug_calculated})

    def get_delete_url(self):
        return reverse('stands:calculated-delete', kwargs={'slug_calculated': self.slug_calculated})


    def save(self, *args, **kwargs):
        self.slug_calculated = gen_slug(self.aim_calculated)
        super(Calculated, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.aim_calculated)

    class Meta:
        verbose_name='Расчетное испытание'
        verbose_name_plural='Расчетные испытания'


class Graph(models.Model):
    name_graph = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название графика',
        db_index=True)
    graph = models.ImageField(
        upload_to=content_graph_name,
        max_length=150,
        verbose_name='График',
        help_text="Разрешенные типы файлов: 'png', 'jpg', 'jpeg', 'gif', 'svg'")
    graph_calculated = models.ForeignKey(
        Calculated,
        on_delete = models.CASCADE,
        related_name='graphs',
        verbose_name = 'Расчетное испытание')


    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         # меняем имя файла и указываем путь
    #         extension_graph = self.graph.name.rsplit('.', 1)[1].lower()
    #         new_name_graph = self.graph_calculated.stand.name_stand + '/graph/' + str(self.graph_calculated.data_calculated) + '/' + self.name_graph + '.' + extension_graph
    #         self.graph.name = new_name_graph
    #     super(Graph, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name_graph)

    class Meta:
        verbose_name='График'
        verbose_name_plural='Графики'

class SettlementFile(models.Model):
    name_settlementfile = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название расчетного файла',
        db_index=True)
    settlementfile = models.FileField(
        upload_to=content_settlementfile_name,
        max_length=150,
        verbose_name='Расчетный файл',
        validators=[validate_report_extension],
        help_text="Недопустимые типы файлов: 'png', 'jpg', 'jpeg', 'gif', 'svg'")
    settlementfile_calculated = models.ForeignKey(
        Calculated,
        on_delete = models.CASCADE,
        related_name='settlementfiles',
        verbose_name = 'Расчетное испытание')

    # def save(self, *args, **kwargs):
    #     # меняем имя файла и указываем путь
    #     if not self.id:
    #         extension_settlementfile = self.settlementfile.name.rsplit('.', 1)[1].lower()
    #         new_name_settlementfile = self.settlementfile_calculated.stand.name_stand + '/settlementfiles/' + str(self.settlementfile_calculated.data_calculated) + '/' + self.name_settlementfile + '.' + extension_settlementfile
    #         self.settlementfile.name = new_name_settlementfile
    #     super(SettlementFile, self).save(*args, **kwargs)


    def __str__(self):
        return "{}".format(self.name_settlementfile)

    class Meta:
        verbose_name='Расчетный файл'
        verbose_name_plural='Расчетные файлы'
