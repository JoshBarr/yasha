# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_homepage_banner_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpostpage',
            options={'verbose_name': 'Blog Post'},
        ),
        migrations.AddField(
            model_name='yashapage',
            name='headline',
            field=models.CharField(default=b'', help_text=b'The page headline', max_length=255),
        ),
    ]
