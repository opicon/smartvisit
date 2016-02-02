# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartvisit', '0004_auto_20160119_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='places',
            name='longitude',
            field=models.FloatField(),
        ),
    ]
