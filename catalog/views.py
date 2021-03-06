import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Case, Count, When
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import RenewBookModelForm
from .models import Author, Book, BookInstance, Genre


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=BookInstance.AVAILABLE).count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_titles_with_the = Book.objects.filter(title__icontains='the ').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'catalog/index.html', context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_titles_with_the': num_titles_with_the,
        'num_visits': num_visits})


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if book_inst.status != BookInstance.ON_LOAN:
        return HttpResponseRedirect(reverse('catalog:all-loaned'))

    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()
            return HttpResponseRedirect(reverse('catalog:all-loaned'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    ctx = {'form': form, 'bookinst': book_inst}
    return render(request, 'catalog/librarian/book-renew.html', ctx)


class BookListView(ListView):
    model = Book
    paginate_by = 10
    queryset = Book.objects.annotate(
            total=Count('id'),
            available=Count(Case(When(bookinstance__status=BookInstance.AVAILABLE, then=1))),
            reserved=Count(Case(When(bookinstance__status=BookInstance.RESERVED, then=1))),
            onloan=Count(Case(When(bookinstance__status=BookInstance.ON_LOAN, then=1))),
            maintenance=Count(Case(When(bookinstance__status=BookInstance.MAINTENANCE, then=1))))


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


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/borrower/loaned-list.html'
    context_object_name = 'bookinstance_list'

    def get_queryset(self):
        return BookInstance.objects\
            .filter(borrower=self.request.user)\
            .filter(status__exact=BookInstance.ON_LOAN)\
            .order_by('due_back')


class AllLoanedBooks(PermissionRequiredMixin, ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/librarian/all-loans.html'
    context_object_name = 'loan_list'

    def get_queryset(self):
        return BookInstance.objects\
            .filter(status__exact=BookInstance.ON_LOAN)\
            .order_by('due_back', 'borrower__id')


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_author'
    model = Author
    fields = '__all__'
    initial = {'date_of_birth': '24/02/1982'}
    template_name = 'catalog/forms/default_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(AuthorCreate, self).get_context_data(**kwargs)
        ctx['operation'] = 'Create'
        ctx['object_type'] = 'Author'
        return ctx


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_author'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/forms/default_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(AuthorUpdate, self).get_context_data(**kwargs)
        ctx['operation'] = 'Update'
        ctx['object_type'] = 'Author'
        return ctx


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_author'
    model = Author
    success_url = reverse_lazy('catalog:authors-list')
    template_name = 'catalog/forms/default_confirm_delete.html'

    def get_context_data(self, **kwargs):
        ctx = super(AuthorDelete, self).get_context_data(**kwargs)
        ctx['back_url'] = reverse_lazy('catalog:author-detail', kwargs={'pk': ctx['object'].id})
        return ctx


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_book'
    model = Book
    fields = '__all__'
    template_name = 'catalog/forms/default_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(BookCreate, self).get_context_data(**kwargs)
        ctx['operation'] = 'Create'
        ctx['object_type'] = 'Book'
        return ctx


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_book'
    model = Book
    fields = '__all__'
    template_name = 'catalog/forms/default_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(BookUpdate, self).get_context_data(**kwargs)
        ctx['operation'] = 'Update'
        ctx['object_type'] = 'Book'
        return ctx


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_book'
    model = Book
    success_url = reverse_lazy('catalog:books-list')
    template_name = 'catalog/forms/default_confirm_delete.html'

    def get_context_data(self, **kwargs):
        ctx = super(BookDelete, self).get_context_data(**kwargs)
        ctx['back_url'] = reverse_lazy('catalog:book-detail', kwargs={'pk': ctx['object'].id})
        return ctx
