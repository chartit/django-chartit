from django.db import models

class Author(models.Model):
    
    first_name = models.CharField(max_length=50, db_column='first_name')
    last_name = models.CharField(max_length=50, db_column='last_name')
    
    def __unicode__(self):
        return '%s %s' %(self.first_name, self.last_name)
    
    class Meta:
        db_table = 'author'


class Publisher(models.Model):
    
    name = models.CharField(max_length=50, db_column='name')
    
    def __unicode__(self):
        return '%s' %(self.name)
    
    class Meta:
        db_table = 'publisher'


class Genre(models.Model):
    
    name = models.CharField(max_length=50, db_column='name')
    
    def __unicode__(self):
        return '%s' %(self.name)
    
    class Meta:
        db_table = 'genre'
        
    
class Book(models.Model):
    
    title = models.CharField(max_length=50, db_column='title')
    rating = models.FloatField(db_column='rating')
    rating_count = models.IntegerField(db_column='rating_count')
    authors = models.ManyToManyField(Author, db_column='authors')
    publisher = models.ForeignKey(Publisher, db_column='publisher', null=True, blank=True, 
                                  on_delete=models.SET_NULL)
    related = models.ManyToManyField('self', db_column='related', blank=True)
    genre = models.ForeignKey(Genre, db_column='genre', null=True, blank=True, 
                                     on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return '%s' %(self.title)
    
    class Meta:
        db_table = 'book'
    
class BookStore(models.Model):
    
    name =  models.CharField(max_length=50, db_column='name')
    city = models.ForeignKey('weather.City')
    
    def __unicode__(self):
        return '%s' %(self.name)
    
    class Meta:
        db_table = 'bookstore'
    
class SalesHistory(models.Model):
    
    bookstore = models.ForeignKey(BookStore, db_column='bookstore')
    book = models.ForeignKey(Book, db_column='book')
    sale_date = models.DateField(db_column='sale_date')
    sale_qty = models.IntegerField(db_column='sale_qty')
    price = models.DecimalField(max_digits=5, decimal_places=2, db_column='price')
    
    def __unicode__(self):
        return '%s %s %s' %(self.bookstore, self.book, self.sale_date)
    
    class Meta:
        db_table = 'saleshistory'
