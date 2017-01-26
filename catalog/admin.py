from django.conf import settings
from django.contrib import admin

from .models import Author, Book, BookInstance, Genre, Language


admin.site.index_title = settings.ADMIN_INDEX_TITLE
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE


class BookInlineAdmin(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ('first_name', 'last_name', ('date_of_birth', 'date_of_death'))
    inlines = [BookInlineAdmin]


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

    def display_genre(self, obj):
        return ', '.join([g.name for g in obj.genre.all()[:3]])

    display_genre.short_description = 'Genre'


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back', 'borrower')}))
    search_fields = ['book__title', 'id']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'books_in_genre')

    @staticmethod
    def books_in_genre(obj):
        return obj.book_set.all().count()


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass
