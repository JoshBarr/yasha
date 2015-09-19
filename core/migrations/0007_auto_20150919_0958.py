# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('core', '0006_homepage_what_we_do_quote'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('body', wagtail.wagtailcore.fields.RichTextField(max_length=255, blank=True)),
                ('image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomeStatistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('statistic', models.CharField(max_length=255, blank=True)),
                ('caption', models.CharField(max_length=255, blank=True)),
                ('image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='issue_image',
            new_name='quote_image',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='issue_body',
            new_name='statistics_body',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='issue_headline',
            new_name='statistics_headline',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='stats_1_number',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='stats_1_text',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='stats_2_number',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='stats_2_text',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='what_we_do_quote',
        ),
        migrations.AddField(
            model_name='homepage',
            name='what_we_do_headline',
            field=models.CharField(default=b'', help_text=b'Top of the what we do section', max_length=255),
        ),
        migrations.AddField(
            model_name='homestatistic',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='statistics', to='core.HomePage'),
        ),
        migrations.AddField(
            model_name='homesection',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='sections', to='core.HomePage'),
        ),
        migrations.AddField(
            model_name='homesection',
            name='page_link',
            field=models.ForeignKey(related_name='+', blank=True, to='wagtailcore.Page', null=True),
        ),
    ]
