from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.http.response import HttpResponse
from django.db.models import Case, Count, When

from .models import Author, Book, BookInstance, Genre


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=BookInstance.AVAILABLE).count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_titles_with_the = Book.objects.filter(title__icontains='the ').count()

    return render(request, 'catalog/index.html', context={
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


class BookListView(ListView):
    model = Book
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author
    queryset = Author.objects.annotate(num_books=Count('book')).all()


class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        ctx = super(AuthorDetailView, self).get_context_data(**kwargs)
        books = ctx['author'].book_set.annotate(
            total=Count('bookinstance'),
            available=Count(Case(When(bookinstance__status=BookInstance.AVAILABLE, then=1))),
            reserved=Count(Case(When(bookinstance__status=BookInstance.RESERVED, then=1))),
            onloan=Count(Case(When(bookinstance__status=BookInstance.ON_LOAN, then=1))),
            maintenance=Count(Case(When(bookinstance__status=BookInstance.MAINTENANCE, then=1))))
        ctx['books'] = books
        return ctx

