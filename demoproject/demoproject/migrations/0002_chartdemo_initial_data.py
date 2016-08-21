# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
from django.db import migrations


def initial_data(apps, _):
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, 'chartdemo.json')

    data = open(path, 'r').read()
    data = json.loads(data)

    for record in data:
        model_class = apps.get_model("demoproject", record['model'])
        obj = model_class(**record['fields'])
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('demoproject', '0001_initial')
    ]

    operations = [
        migrations.RunPython(initial_data),
    ]
