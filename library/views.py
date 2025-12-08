from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q, Sum, Max, Min
from .models import Author, Book
from .serializers import (
    AuthorSerializer, AuthorListSerializer,
    BookSerializer, BookListSerializer
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'nationality', 'email']
    ordering_fields = ['last_name', 'first_name', 'birth_date', 'created_at']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorListSerializer
        return AuthorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Optimize queries by prefetching related books
        queryset = queryset.prefetch_related('books')

        # Filter by nationality if provided
        nationality = self.request.query_params.get('nationality', None)
        if nationality:
            queryset = queryset.filter(nationality__icontains=nationality)

        return queryset

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Advanced query: Get statistics about authors using aggregation.
        Returns total authors, authors with books, and average books per author.
        """
        stats = Author.objects.aggregate(
            total_authors=Count('id'),
            authors_with_books=Count('id', filter=Q(books__isnull=False), distinct=True),
            avg_books_per_author=Avg('books__id')
        )

        # Get most prolific authors (those with most books)
        prolific_authors = Author.objects.annotate(
            book_count=Count('books')
        ).filter(book_count__gt=0).order_by('-book_count')[:5]

        prolific_data = AuthorListSerializer(prolific_authors, many=True).data

        return Response({
            'statistics': stats,
            'most_prolific_authors': prolific_data
        })

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """
        Get all books by a specific author.
        """
        author = self.get_object()
        books = author.books.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'isbn', 'publisher', 'description', 'authors__first_name', 'authors__last_name']
    ordering_fields = ['title', 'publication_date', 'price', 'rating', 'created_at']
    ordering = ['-publication_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Optimize queries by prefetching related authors
        queryset = queryset.prefetch_related('authors')

        # Filter by genre if provided
        genre = self.request.query_params.get('genre', None)
        if genre:
            queryset = queryset.filter(genre=genre)

        # Filter by in_stock status
        in_stock = self.request.query_params.get('in_stock', None)
        if in_stock is not None:
            if in_stock.lower() == 'true':
                queryset = queryset.filter(stock_quantity__gt=0)
            elif in_stock.lower() == 'false':
                queryset = queryset.filter(stock_quantity=0)

        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Filter by minimum rating
        min_rating = self.request.query_params.get('min_rating', None)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        return queryset

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Advanced query: Get comprehensive book statistics using aggregation.
        Includes counts, averages, and grouping by genre.
        """
        # Overall statistics
        overall_stats = Book.objects.aggregate(
            total_books=Count('id'),
            avg_price=Avg('price'),
            max_price=Max('price'),
            min_price=Min('price'),
            avg_rating=Avg('rating'),
            total_stock=Sum('stock_quantity'),
            avg_pages=Avg('page_count')
        )

        # Statistics by genre
        genre_stats = Book.objects.values('genre').annotate(
            count=Count('id'),
            avg_price=Avg('price'),
            avg_rating=Avg('rating')
        ).order_by('-count')

        # Books with multiple authors
        multi_author_books = Book.objects.annotate(
            author_count=Count('authors')
        ).filter(author_count__gt=1).count()

        return Response({
            'overall_statistics': overall_stats,
            'statistics_by_genre': genre_stats,
            'books_with_multiple_authors': multi_author_books
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """
        Get top-rated books (rating >= 4.0) with author count.
        Advanced query using annotation and filtering.
        """
        top_books = Book.objects.annotate(
            author_count=Count('authors')
        ).filter(
            rating__gte=4.0
        ).order_by('-rating', '-publication_date')[:10]

        serializer = BookListSerializer(top_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent_releases(self, request):
        """
        Get recent book releases (last year) with complex filtering.
        Advanced query using Q objects and annotations.
        """
        from datetime import datetime, timedelta

        one_year_ago = datetime.now().date() - timedelta(days=365)

        recent_books = Book.objects.annotate(
            author_count=Count('authors')
        ).filter(
            Q(publication_date__gte=one_year_ago) &
            (Q(stock_quantity__gt=0) | Q(rating__gte=4.0))
        ).order_by('-publication_date')

        serializer = BookListSerializer(recent_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_author(self, request):
        """
        Get books grouped by author count.
        Shows distribution of single-author vs multi-author books.
        """
        books_by_author_count = Book.objects.annotate(
            author_count=Count('authors')
        ).values('author_count').annotate(
            book_count=Count('id')
        ).order_by('author_count')

        return Response({
            'distribution': list(books_by_author_count)
        })
