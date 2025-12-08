from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'birth_date',
            'nationality', 'biography', 'email', 'book_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_book_count(self, obj):
        return obj.books.count()


class AuthorListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = ['id', 'full_name', 'nationality']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorListSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Author.objects.all(),
        source='authors'
    )
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'authors', 'author_ids', 'genre',
            'publication_date', 'publisher', 'page_count', 'language',
            'description', 'price', 'stock_quantity', 'rating',
            'is_in_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_isbn(self, value):
        if not value.isdigit() or len(value) not in [10, 13]:
            raise serializers.ValidationError(
                "ISBN must be 10 or 13 digits."
            )
        return value


class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorListSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'authors', 'genre',
            'publication_date', 'price', 'rating'
        ]
