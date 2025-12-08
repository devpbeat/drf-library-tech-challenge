from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'nationality', 'birth_date', 'email', 'book_count']
    list_filter = ['nationality', 'birth_date']
    search_fields = ['first_name', 'last_name', 'email', 'nationality']
    ordering = ['last_name', 'first_name']
    date_hierarchy = 'birth_date'

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'birth_date', 'nationality', 'email')
        }),
        ('Biography', {
            'fields': ('biography',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'genre', 'publication_date', 'publisher',
                    'price', 'stock_quantity', 'rating', 'is_in_stock']
    list_filter = ['genre', 'publication_date', 'language', 'authors']
    search_fields = ['title', 'isbn', 'publisher', 'description']
    ordering = ['-publication_date', 'title']
    date_hierarchy = 'publication_date'
    filter_horizontal = ['authors']

    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'isbn', 'authors', 'genre', 'language')
        }),
        ('Publication Details', {
            'fields': ('publication_date', 'publisher', 'page_count')
        }),
        ('Sales Information', {
            'fields': ('price', 'stock_quantity', 'rating')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'is_in_stock']

    def is_in_stock(self, obj):
        return obj.is_in_stock
    is_in_stock.boolean = True
    is_in_stock.short_description = 'In Stock'
