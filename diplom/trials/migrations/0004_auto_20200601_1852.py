# Generated by Django 3.0.6 on 2020-06-01 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stands', '0001_initial'),
        ('trials', '0003_experimental_testobjects'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='experimental',
            unique_together={('aim_experimental', 'stand', 'data_experimental')},
        ),
    ]
