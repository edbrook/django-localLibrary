from django.contrib import admin

from .models import Author, Book, BookInstance, Genre, Language


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
    list_display = ('id', 'display_book_title', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back')}))
    search_fields = ['book__title', 'id']

    def display_book_title(self, obj):
        return obj.book.title

    display_book_title.short_description = 'Book'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass
