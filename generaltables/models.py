from django.db import models
from django.urls import reverse
import os
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Проверка значений параметров(только цифры + доп. знаки)
def validate_number(value):
    s = '0123456789'
    for v in value:
        if v not in s:
            raise ValidationError(
                _('В данном поле могут быть только цифры.'),
                code='error_number',
            )

# Проверка расширения для документов
def validate_report_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
    if ext.lower() in valid_extensions:
        raise ValidationError(
        _('Неподдерживаемое расширение файла.'),
        code='error_file',
        )

# Проверка значений параметров(только цифры + доп. знаки)
def validate_number_parameter(value):
    s = '0123456789-^.x'
    for v in value:
        if v not in s:
            raise ValidationError(
                _('В данном поле могут быть только цифры и знаки: " - ", " ^ ", " . ", " x "'),
                code='error_number_parameter',
            )

# меняем имя файла и указываем путь
def content_report_name(instance, filename):
    extension_report = instance.report.name.rsplit('.', 1)[1].lower()

    if instance.report_experimental is not None:
        new_name_report = 'trials/' + instance.report_experimental.stand.name_stand + '/report/' + str(instance.report_experimental.data_experimental) + '/' + instance.name_report + '.' + extension_report
        instance.report.name = new_name_report

    if instance.report_calculated is not None:
        new_name_report = 'calculatedtrials/' + instance.report_calculated.stand.name_stand + '/report/' + str(instance.report_calculated.data_calculated) + '/' + instance.name_report + '.' + extension_report
        instance.report.name = new_name_report
    return "{subfolder}".format(subfolder=instance.report.name)

# def validate_words(value):
#     s = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
#     for v in value:
#         if v not in s:
#             raise ValidationError(
#                 _('В данном поле кириллица'),
#                 code='error_number_parameter',
#             )

class Tester(models.Model):
    last_name = models.CharField(
        max_length=30,
        verbose_name='Фамилия',
        db_index=True)
    first_name = models.CharField(
        max_length=20,
        verbose_name='Имя',
        db_index=True)
    middle_name = models.CharField(
        max_length=30,
        verbose_name='Отчество',
        db_index=True)
    department = models.CharField(
        max_length=10,
        verbose_name='Номер отдела',
        validators=[validate_number])
    post = models.CharField(
        max_length=70,
        verbose_name='Должность')

    def save(self, *args, **kwargs):
        self.last_name = self.last_name.capitalize()
        self.first_name = self.first_name.capitalize()
        self.middle_name = self.middle_name.capitalize()
        self.post = self.post.capitalize()
        super(Tester, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s %s %s %s" % (
            self.last_name,
            self.first_name,
            self.middle_name,
            self.department,
            self.post)

    class Meta:
        verbose_name='Испытатель'
        verbose_name_plural='Испытатели'
        unique_together = ("last_name", "first_name", "middle_name", "department", "post")
        ordering = ['last_name', 'first_name', 'middle_name']

class TestObject(models.Model):
    title_object = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='Название объкта испытания')


    # def clean(self):
    #     # Проверки для того, чтобы одно из полей было заполнено
    #     if self.objects_experimental is None and self.object_calculated is None:
    #         raise ValidationError(_('Выберите экспериментальное или расчетное испытание.'))

        # if self.objects_experimental is not None and self.object_calculated is not None:
        #     raise ValidationError(_('Объект испытание не может быть утсановлен для экспериментального и расчетного испытания одновременно.'))

    def __str__(self):
        return "{}".format(self.title_object)

    class Meta:
        verbose_name='Объект испытания'
        verbose_name_plural='Объeкты испытания'
        ordering = ['title_object']

class ParameterObject(models.Model):
    testobject = models.ForeignKey(
        TestObject,
        on_delete = models.CASCADE,
        related_name='parameters_object',
        verbose_name = 'Объект испытания')
    name_parametr_object = models.CharField(
        max_length=100,
        verbose_name='Название параметра')
    value_parametr_object  = models.CharField(
        max_length=20,
        validators=[validate_number_parameter],
        blank = True,
        verbose_name='Значение параметра')
    measure_parametr_object  = models.CharField(
        max_length=10,
        blank = True,
        verbose_name='Единица измерения')

    def save(self, *args, **kwargs):
        self.name_parametr_object = self.name_parametr_object.capitalize()
        super(ParameterObject, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s %s" % (self.name_parametr_object, self.value_parametr_object, self.measure_parametr_object )

    class Meta:
        verbose_name='Параметр объекта испытания'
        verbose_name_plural='Параметры объекта испытания'
        unique_together = ("testobject", "name_parametr_object", "value_parametr_object", "measure_parametr_object")


class Report(models.Model):
    name_report = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название файла')
    report = models.FileField(
        upload_to=content_report_name,
        max_length=150,
        validators=[validate_report_extension],
        help_text="Разрешенные типы файлов: 'rar', 'pdf', 'doc', 'txt' и т.д.",
        verbose_name='Файл')
    report_experimental = models.ForeignKey(
        'trials.Experimental',
        on_delete = models.SET_NULL,
        related_name='reports_experimental',
        blank=True,
        null=True,
        verbose_name = 'Экспериментальное испытание')
    report_calculated = models.ForeignKey(
        'calculatedtrials.Calculated',
        on_delete = models.SET_NULL,
        related_name='reports_calculated',
        blank=True,
        null=True,
        verbose_name = 'Расчетное испытание')

    def clean(self):
        # Проверки для того, чтобы одно из полей было заполнено
        if self.report_experimental is None and self.report_calculated is None:
            raise ValidationError(_('Выберите экспериментальное или расчетное испытание.'))

        # if self.report_experimental is not None and self.report_calculated is not None:
        #     raise ValidationError(_('Объект испытание не может быть утсановлен для экспериментального и расчетного испытания одновременно.'))

    # def save(self, *args, **kwargs):
    #
    #     # меняем имя файла и указываем путь
    #     # extension_report = self.report.name.rsplit('.', 1)[1].lower()
    #     #
    #     # if not self.id:
    #     #     if self.report_experimental is not None:
    #     #         new_name_report = 'trials/' + self.report_experimental.stand.name_stand + '/report/' + str(self.report_experimental.data_experimental) + '/' + self.name_report + '.' + extension_report
    #     #         self.report.name = new_name_report
    #     #
    #     #     if self.report_calculated is not None:
    #     #         new_name_report = 'calculatedtrials/' + self.report_calculated.stand.name_stand + '/report/' + str(self.report_calculated.data_calculated) + '/' + self.name_report + '.' + extension_report
    #     #         self.report.name = new_name_report
    #
    #     super(Report, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.name_report)

    class Meta:
        verbose_name='Технический отчет и отчетная документация'
        verbose_name_plural='Технические отчеты и отчетные документации'
