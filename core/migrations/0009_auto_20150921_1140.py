# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_footer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='footer',
            options={'verbose_name': 'Footer content'},
        ),
        migrations.AddField(
            model_name='yashapage',
            name='large_banner',
            field=models.BooleanField(default=False, help_text=b'Whether or not the banner should be a big one'),
        ),
        migrations.AlterField(
            model_name='homesection',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(max_length=700, blank=True),
        ),
    ]
