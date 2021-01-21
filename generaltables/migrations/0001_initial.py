# Generated by Django 3.0.6 on 2020-05-31 21:06

from django.db import migrations, models
import django.db.models.deletion
import generaltables.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trials', '0001_initial'),
        ('calculatedtrials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_object', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Название объкта испытания')),
            ],
            options={
                'verbose_name': 'Объект испытания',
                'verbose_name_plural': 'Объeкты испытания',
            },
        ),
        migrations.CreateModel(
            name='Tester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(db_index=True, max_length=30, verbose_name='Фамилия')),
                ('first_name', models.CharField(db_index=True, max_length=20, verbose_name='Имя')),
                ('middle_name', models.CharField(db_index=True, max_length=30, verbose_name='Отчество')),
                ('department', models.CharField(max_length=10, validators=[generaltables.models.validate_number], verbose_name='Номер отдела')),
                ('post', models.CharField(max_length=70, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Испытатель',
                'verbose_name_plural': 'Испытатели',
                'unique_together': {('last_name', 'first_name', 'middle_name', 'department', 'post')},
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_report', models.CharField(max_length=150, unique=True, verbose_name='Название файла')),
                ('report', models.FileField(help_text="Разрешенные типы файлов: 'rar', 'pdf', 'doc', 'txt' и т.д.", max_length=150, upload_to='', validators=[generaltables.models.validate_report_extension], verbose_name='Файл')),
                ('report_calculated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_calculated', to='calculatedtrials.Calculated', verbose_name='Расчетное испытание')),
                ('report_experimental', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_experimental', to='trials.Experimental', verbose_name='Экспериментальное испытание')),
            ],
            options={
                'verbose_name': 'Технический отчет и отчетная документация',
                'verbose_name_plural': 'Технические отчеты и отчетные документации',
            },
        ),
        migrations.CreateModel(
            name='ParameterObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_parametr_object', models.CharField(max_length=100, verbose_name='Название параметра')),
                ('value_parametr_object', models.CharField(blank=True, max_length=20, validators=[generaltables.models.validate_number_parameter], verbose_name='Значение параметра')),
                ('measure_parametr_object', models.CharField(blank=True, max_length=10, verbose_name='Единица измерения')),
                ('testobject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters_object', to='generaltables.TestObject', verbose_name='Объект испытания')),
            ],
            options={
                'verbose_name': 'Параметр объекта испытания',
                'verbose_name_plural': 'Параметры объекта испытания',
                'unique_together': {('testobject', 'name_parametr_object', 'value_parametr_object', 'measure_parametr_object')},
            },
        ),
    ]