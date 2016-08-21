# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import migrations


def initialize_data(apps, _):
    """
        This migration adds some unicode data, which is displayed in
        already existing Pivot charts to address rendering of unicode
        values.

        The new city is the Cyrillic transcription of Houston and the
        book is an old child's book from the mid 80s. All the Cyrillic
        texts are in Bulgarian for those who may wonder.

        At the moment all Pivot charts display data for this new city
        b/c all of them use SalesHistory as data source and generally
        render the information based on city! Existing tests are confirmed
        to break when Issue #5 is not fixed and pass when it is!
    """
    Author = apps.get_model("demoproject", "Author")
    author = Author.objects.create(first_name="Венелин", last_name="Вълканов")

    Genre = apps.get_model("demoproject", "Genre")
    genre = Genre.objects.create(name="Детска фантастика")

    Publisher = apps.get_model("demoproject", "Publisher")
    Book = apps.get_model("demoproject", "Book")
    book = Book.objects.create(title="Трак", rating=6.0, rating_count=10,
                               genre=genre, publisher=Publisher.objects.last())
    book.authors.add(author)

    City = apps.get_model("demoproject", "City")
    city = City.objects.create(city="Хюстън", state="TX")

    BookStore = apps.get_model("demoproject", "BookStore")
    book_store = BookStore.objects.create(name="Книжарницата на Марио",
                                          city=city)

    SalesHistory = apps.get_model("demoproject", "SalesHistory")
    # add sales history for the book with unicode title and genre
    SalesHistory.objects.create(bookstore=book_store, book=book,
                                sale_date=datetime.now(), sale_qty=3000,
                                price=4.20)
    # add history for another book from the existing list in DB
    SalesHistory.objects.create(bookstore=book_store,
                                book=Book.objects.first(),
                                sale_date=datetime.now(), sale_qty=2000,
                                price=2.40)


class Migration(migrations.Migration):

    dependencies = [
        ('demoproject', '0003_pivotdemo_initial_data')
    ]

    operations = [
        migrations.RunPython(initialize_data),
    ]
