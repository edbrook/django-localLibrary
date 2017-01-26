import uuid
from datetime import date

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a book genre (e.g. Science Fiction)")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)


class Language(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField('ISBN', max_length=20, unique=True)
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])

    def get_instance_count(self):
        return self.bookinstance_set.count()

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    MAINTENANCE = 'm'
    ON_LOAN = 'l'
    AVAILABLE = 'a'
    RESERVED = 'r'
    LOAN_STATUS_CHOICES = ((MAINTENANCE, 'maintenance'),
                           (ON_LOAN, 'on loan'),
                           (AVAILABLE, 'available'),
                           (RESERVED, 'reserved'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=50)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=LOAN_STATUS_CHOICES, blank=True, default=MAINTENANCE)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']

    @property
    def is_overdue(self):
        return date.today() > self.due_back

    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.book.id)])

    def __str__(self):
        return '[{}] {}'.format(self.id, self.book.title)
