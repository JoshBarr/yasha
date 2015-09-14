# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150915_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='what_we_do_quote',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
    ]
