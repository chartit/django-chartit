# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
from django.db import migrations


def initial_data(apps, _):
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, 'pivotdemo.json')

    data = open(path, 'r').read()
    data = json.loads(data)

    Book = apps.get_model("demoproject", "Book")
    BookRelated = None
    BookAuthors = None
    for relation in Book._meta.many_to_many:
        if relation.name == 'related':
            try:
                BookRelated = relation.remote_field.through
            except AttributeError:
                # available in Django 1.8
                BookRelated = relation.rel.through

        if relation.name == 'authors':
            try:
                BookAuthors = relation.remote_field.through
            except AttributeError:
                # available in Django 1.8
                BookAuthors = relation.rel.through

    # create objects which don't have FKs or ManyToMany fields
    for record in data:
        # Book has ManyToMany relation to itself
        if record['model'] in ['Book', 'BookStore', 'SalesHistory']:
            continue

        model_class = apps.get_model("demoproject", record['model'])
        obj = model_class(**record['fields'])
        obj.pk = record['pk']
        obj.save()

    # create Book objects
    for record in data:
        # skip everything which isn't a book
        if record['model'] != 'Book':
            continue

        # build a list of book authors using the intermediate
        # BookAuthors table
        for author_id in record['fields']['authors']:
            author_obj = BookAuthors()
            author_obj.book_id = record['pk']
            author_obj.author_id = author_id
            author_obj.save()
        del record['fields']['authors']

        # build a list of related books
        # fill data for the intermediate BookRelated table
        # due to circular dependencies in the data
        for related_id in record['fields']['related']:
            related_obj = BookRelated()
            related_obj.from_book_id = record['pk']
            related_obj.to_book_id = related_id
            related_obj.save()
        del record['fields']['related']

        model_class = apps.get_model("demoproject", record['model'])
        obj = model_class(**record['fields'])
        obj.pk = record['pk']
        obj.save()

    # now populate the obkects which hold FKs on Book
    for record in data:
        if record['model'] not in ['BookStore', 'SalesHistory']:
            continue

        model_class = apps.get_model("demoproject", record['model'])
        obj = model_class(**record['fields'])
        obj.pk = record['pk']
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('demoproject', '0002_chartdemo_initial_data')
    ]

    operations = [
        migrations.RunPython(initial_data),
    ]
