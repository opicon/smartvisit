# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartvisit', '0006_places_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='places',
            name='rating',
        ),
        migrations.AddField(
            model_name='places',
            name='description',
            field=models.CharField(default='...', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='places',
            name='photo',
            field=models.CharField(default='...', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='places',
            name='wikipedia',
            field=models.CharField(default='...', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='places',
            name='categorie',
            field=models.CharField(choices=[('monument', 'monument'), ('nature', 'nature'), ('art', 'art')], max_length=15),
        ),
    ]
