from django.db import models
from stands.models import Stand
from django.urls import reverse

from django.utils.text import slugify
from time import time

import os
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _


# Генерируем slug
def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug.upper() + "-" + str(int(time()))



class Experimental(models.Model):
    aim_experimental = models.CharField(
        max_length=250,
        verbose_name='Цель экспериментального испытания',
        db_index=True)
    slug_experimental = models.SlugField(
        max_length=250,
        blank=True,
        unique=True)
    stand = models.ForeignKey(
        Stand,
        on_delete = models.CASCADE,
        related_name='experimentals_1',
        verbose_name = 'Стенд')
    testobjects = models.ManyToManyField(
        'generaltables.TestObject',
        related_name='objects_experimental',
        verbose_name = 'Объект испытания')
    testers = models.ManyToManyField(
        'generaltables.Tester',
        related_name='experimentals_tester',
        verbose_name = 'Испытатель')
    data_experimental = models.DateField(
        verbose_name='Дата экспериментального испытания',
        db_index=True,
        help_text="Введите дату по данному формату: <em>DD.MM.YYYY</em>")

    def get_detail_url(self):
        return reverse('stands:experimental-detail', kwargs={'slug_stand': self.stand.slug_stand, 'slug_experimental': self.slug_experimental})

    def get_edit_url(self):
        return reverse('stands:experimental-edit', kwargs={'slug_experimental': self.slug_experimental})

    def get_delete_url(self):
        return reverse('stands:experimental-delete', kwargs={'slug_experimental': self.slug_experimental})

    #
    # def get_absolute_url(self):
    #     return reverse('blog:post_detail', args=[self.publish.year,                       self.publish.month, self.publish.day, self.slug])

    def save(self, *args, **kwargs):
        self.slug_experimental = gen_slug(self.aim_experimental)
        super(Experimental, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.aim_experimental)

    class Meta:
        unique_together = (("aim_experimental", "stand", "data_experimental"),)
        verbose_name='Экспериментальное испытание'
        verbose_name_plural='Экспериментальные испытания'
