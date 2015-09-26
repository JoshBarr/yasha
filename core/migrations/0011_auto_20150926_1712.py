# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('core', '0010_footer_partner_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='footer',
            options={'verbose_name': 'Footer'},
        ),
        migrations.AddField(
            model_name='homepage',
            name='feed_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
        ),
    ]
