from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    GENRE_CHOICES = [
        ('FICTION', 'Fiction'),
        ('NON_FICTION', 'Non-Fiction'),
        ('MYSTERY', 'Mystery'),
        ('THRILLER', 'Thriller'),
        ('ROMANCE', 'Romance'),
        ('SCIENCE_FICTION', 'Science Fiction'),
        ('FANTASY', 'Fantasy'),
        ('BIOGRAPHY', 'Biography'),
        ('HISTORY', 'History'),
        ('SELF_HELP', 'Self Help'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    authors = models.ManyToManyField(Author, related_name='books')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='OTHER')
    publication_date = models.DateField()
    publisher = models.CharField(max_length=200)
    page_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    language = models.CharField(max_length=50, default='English')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_date', 'title']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['title']),
            models.Index(fields=['-publication_date']),
        ]

    def __str__(self):
        return self.title

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
