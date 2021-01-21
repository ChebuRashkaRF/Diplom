from django.db import models
from django.urls import reverse

from django.utils.text import slugify
from time import time

# import os
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _

# Проверка значений параметров(только цифры + доп. знаки)
def validate_number(value):
    s = '0123456789-^.x'
    for v in value:
        if v not in s:
            raise ValidationError(
                _('В данном поле могут быть только цифры и знаки: " - ", " ^ ", " . ", " x "'),
                code='error_number',
            )

# # Проверка расширения для изображений
# def validate_img_extension(value):
#     ext = os.path.splitext(value.name)[1]
#     valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
#     if not ext.lower() in valid_extensions:
#         raise ValidationError(
#         _('Неподдерживаемое расширение файла.'),
#         code='error_img',
#         )
#
# # Проверка расширения для документов
# def validate_file_extension(value):
#     ext = os.path.splitext(value.name)[1]
#     valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
#     if ext.lower() in valid_extensions:
#         raise ValidationError(
#         _('Неподдерживаемое расширение файла.'),
#         code='error_file',
#         )

# Генерируем slug
def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug.upper() + "-" + str(int(time()))

# def document_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     initial_path = instance.document.path
#     extension = instance.document.name.rsplit('.', 1)[1].lower()
#     new_name_file = instance.name_document + '.' + extension
#     return 'stands/document/{0}'.format(new_name_file)



class Stand(models.Model):
    name_stand = models.CharField(
        max_length=40,
        unique=True,
        verbose_name='Название стенда')
    slug_stand = models.SlugField(
        max_length=200,
        blank=True,
        unique=True)

    def get_experimental_url(self):
        return reverse('stands:experimental-stand', kwargs={'slug_stand': self.slug_stand})

    def get_calculated_url(self):
        return reverse('stands:calculated-stand', kwargs={'slug_stand': self.slug_stand})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_stand = gen_slug(self.name_stand)
        super(Stand, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name_stand)

    class Meta:
        verbose_name='Стенд'
        verbose_name_plural='Стенды'


class DocumentStand(models.Model):
    stand = models.ForeignKey(
        Stand,
        on_delete = models.CASCADE,
        related_name='documents',
        verbose_name = 'Стенд')
    name_document = models.CharField(
        max_length=100,
        unique=True,
        # validators=[validate_unique],
        verbose_name='Название файла документа')
    document = models.FileField(
        upload_to='stands/document/',
        max_length=150,
        # validators=[validate_file_extension],
        # help_text="Разрешенные типы файлов: 'rar', 'pdf', 'doc', 'txt' и т.д.",
        verbose_name='Файл документа')
    # name_img = models.CharField(
    #     max_length=100,
    #     unique=True,

    #
    #     # validators=[validate_unique],
    #     verbose_name='Название файла изображения')
    # img = models.ImageField(
    #     upload_to='stands/',
    #     max_length=150,

    #
    #     validators=[validate_img_extension],
    #     help_text="Разрешенные типы файлов: 'png', 'jpg', 'jpeg', 'gif', 'svg'",
    #     verbose_name='Файл изображения')


    def save(self, *args, **kwargs):


        # меняем имя файла и указываем путь
        if not self.id:
            extension_file = self.document.name.rsplit('.', 1)[1].lower()
            new_name_file = self.stand.name_stand + '/' +  self.name_document + '.' + extension_file
            self.document.name = new_name_file

        # # меняем имя изображения и указываем путь
        # extension_img = self.img.name.rsplit('.', 1)[1].lower()
        # new_name_img = self.stand.name_stand + '/document/' +  self.name_img + '.' + extension
        # self.img.name = new_name_img


        super(DocumentStand, self).save(*args, **kwargs)


    def __str__(self):
        return "{}".format(self.name_document)

    class Meta:
        verbose_name='Докуметация, схема стенда'
        verbose_name_plural='Документации, схемы стенда'

class ParameterStand(models.Model):
    stand = models.ForeignKey(
        Stand,
        on_delete = models.CASCADE,
        related_name='parameters_stand',
        verbose_name = 'Стенд')
    name_parametr_stand = models.CharField(
        max_length=50,
        verbose_name='Название параметра')
    value_parametr_stand = models.CharField(
        max_length=20,
        validators=[validate_number],
        blank = True,
        verbose_name='Значение параметра')
    measure_parametr_stand = models.CharField(
        max_length=10,
        blank = True,
        verbose_name='Единица измерения')


    def save(self, *args, **kwargs):
        self.name_parametr_stand = self.name_parametr_stand.capitalize()
        super(ParameterStand, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s %s" % (self.name_parametr_stand, self.value_parametr_stand, self.measure_parametr_stand )

    class Meta:
        verbose_name='Параметр стенда'
        verbose_name_plural='Параметры стенда'
        unique_together = ("stand", "name_parametr_stand", "value_parametr_stand", "measure_parametr_stand")
