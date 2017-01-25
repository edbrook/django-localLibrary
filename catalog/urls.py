from django.conf.urls import url
from . import views

app_name = 'catalog'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^books/$', views.book, name="books_list"),
    url(r'^authors/$', views.author, name="authors_list"),
    url(r'^books/(?P<pk>\d{1,6})$', views.book, name="book_detail"),
    url(r'^authors/(?P<pk>\d{1,6})$', views.author, name="author_detail"),
]
