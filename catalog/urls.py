from django.conf.urls import url
from . import views

app_name = 'catalog'

urlpatterns = [
    url(r'^$', views.index, name="index"),

    url(r'^books/$', views.BookListView.as_view(), name="books-list"),
    url(r'^book/(?P<pk>\d{1,6})$', views.BookDetailView.as_view(), name="book-detail"),
    url(r'^book/(?P<pk>[-0-9a-f]{36})/renew$', views.renew_book_librarian, name="renew-book-librarian"),

    url(r'^authors/$', views.AuthorListView.as_view(), name="authors-list"),
    url(r'^author/(?P<pk>\d{1,6})$', views.AuthorDetailView.as_view(), name="author-detail"),
    url(r'^author/create$', views.AuthorCreate.as_view(), name='author-create'),
    url(r'^author/(?P<pk>\d{1,6})/update$', views.AuthorUpdate.as_view(), name='author-update'),
    url(r'^author/(?P<pk>\d{1,6})/delete$', views.AuthorDelete.as_view(), name='author-delete'),

    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name="user-loaned"),

    url(r'^all-loans/$', views.AllLoanedBooks.as_view(), name="all-loaned"),
]
