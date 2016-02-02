# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartvisit', '0003_places_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='latitude',
            field=models.DecimalField(decimal_places=8, max_digits=10, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='places',
            name='longitude',
            field=models.DecimalField(decimal_places=8, max_digits=10, default=0),
            preserve_default=False,
        ),
    ]
