# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartvisit', '0002_places_ville'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='rating',
            field=models.CharField(max_length=42, default='defaut'),
            preserve_default=False,
        ),
    ]
