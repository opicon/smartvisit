# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartvisit', '0005_auto_20160119_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
