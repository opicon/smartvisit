# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartvisit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='ville',
            field=models.CharField(max_length=100, default='place'),
            preserve_default=False,
        ),
    ]
