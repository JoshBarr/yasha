# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150914_2013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='yashapage',
            options={'verbose_name': 'Yasha standard page'},
        ),
        migrations.AddField(
            model_name='homepage',
            name='headline',
            field=models.CharField(default=b'', help_text=b'Displayed in the banner', max_length=255),
        ),
        migrations.AlterField(
            model_name='yashapage',
            name='comments',
            field=models.BooleanField(default=False, help_text=b'Comments are off by default. Check the box if you would like to enable them for this         page.', verbose_name=b'Comments ON/OFF'),
        ),
        migrations.AlterField(
            model_name='yashapage',
            name='headline',
            field=models.CharField(default=b'', help_text=b'The page headline, it can be used like a longer title (optional)', max_length=255, blank=True),
        ),
    ]
