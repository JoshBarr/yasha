# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150921_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='partner_text',
            field=wagtail.wagtailcore.fields.RichTextField(max_length=255, blank=True),
        ),
    ]
