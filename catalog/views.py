from django.shortcuts import render
from django.http.response import HttpResponse

from .models import Author, Book, BookInstance, Genre


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=BookInstance.AVAILABLE).count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_titles_with_the = Book.objects.filter(title__icontains='the').count()

    return render(request, 'index.html', context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_titles_with_the': num_titles_with_the})


def book(request, pk=None):
    if pk is None:
        return HttpResponse(content='BOOK_LIST')
    return HttpResponse(content='BOOK_DETAIL')


def author(request, pk=None):
    if pk is None:
        return HttpResponse(content='AUTHOR_LIST')
    return HttpResponse(content='AUTHOR_DETAIL')
