# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('yashapage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.YashaPage')),
            ],
            options={
                'verbose_name': 'About Page',
                'description': 'About Yasha',
            },
            bases=('core.yashapage',),
        ),
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('yashapage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.YashaPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.yashapage',),
        ),
        migrations.CreateModel(
            name='BlogPostPage',
            fields=[
                ('yashapage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.YashaPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.yashapage',),
        ),
        migrations.CreateModel(
            name='ContactPage',
            fields=[
                ('yashapage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.YashaPage')),
            ],
            options={
                'verbose_name': 'Contact Page',
                'description': 'Contact information for Yasha',
            },
            bases=('core.yashapage',),
        ),
        migrations.CreateModel(
            name='DonatePage',
            fields=[
                ('yashapage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.YashaPage')),
            ],
            options={
                'verbose_name': 'Donations Page',
                'description': 'The main donations page',
            },
            bases=('core.yashapage',),
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='body',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='date',
        ),
        migrations.AddField(
            model_name='homepage',
            name='citation',
            field=models.CharField(default=b'', help_text=b'Who authored the quote', max_length=255),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro',
            field=models.CharField(default=b'', help_text=b'Displayed below the headline', max_length=255),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro_button_label',
            field=models.CharField(default=b'', help_text=b'Displayed in the banner area', max_length=128),
        ),
        migrations.AddField(
            model_name='homepage',
            name='issue_body',
            field=models.CharField(default=b'', help_text=b'Body text for the issue block', max_length=255),
        ),
        migrations.AddField(
            model_name='homepage',
            name='issue_headline',
            field=models.CharField(default=b'', help_text=b'Headline for the issue block', max_length=255),
        ),
        migrations.AddField(
            model_name='homepage',
            name='issue_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote',
            field=models.CharField(default=b'', help_text=b'The big homepage quote', max_length=255),
        ),
        migrations.AddField(
            model_name='homepage',
            name='stats_1_number',
            field=models.CharField(default=b'', help_text=b'Statistic', max_length=20),
        ),
        migrations.AddField(
            model_name='homepage',
            name='stats_1_text',
            field=models.CharField(default=b'', help_text=b'Statistic description', max_length=255),
        ),
        migrations.AddField(
            model_name='homepage',
            name='stats_2_number',
            field=models.CharField(default=b'', help_text=b'Statistic 2 (optional)', max_length=20),
        ),
        migrations.AddField(
            model_name='homepage',
            name='stats_2_text',
            field=models.CharField(default=b'', help_text=b'Statistic description 2 (optional)', max_length=255),
        ),
        migrations.AddField(
            model_name='yashapage',
            name='banner_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
        ),
        migrations.AlterField(
            model_name='yashapage',
            name='comments',
            field=models.BooleanField(default=False, help_text=b'Comments are enabled by default. Uncheck the box if you would like to disable them for this         page.', verbose_name=b'Comments ON/OFF'),
        ),
    ]
