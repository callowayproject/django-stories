# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='Slug'),
            preserve_default=True,
        ),
    ]
