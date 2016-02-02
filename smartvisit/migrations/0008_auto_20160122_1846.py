# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartvisit', '0007_auto_20160122_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='categorie',
            field=models.CharField(choices=[('monument', 'monument'), ('nature', 'nature'), ('art', 'art'), ('quartier', 'quartier'), ('insolite', 'insolite'), ('restaurant', 'restaurant')], max_length=15),
        ),
        migrations.AlterField(
            model_name='places',
            name='description',
            field=models.CharField(max_length=1000),
        ),
    ]
