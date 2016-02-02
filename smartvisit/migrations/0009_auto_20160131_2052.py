# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartvisit', '0008_auto_20160122_1846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='places',
            old_name='addresse',
            new_name='adresse',
        ),
    ]
