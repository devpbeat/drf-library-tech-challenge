*Read this in other languages: [English](README.md), [Español](README.es.md)*

# Library Management System

A Django REST Framework application for managing books and authors with a many-to-many relationship.

## Features

- **Data Models**: Book and Author models with many-to-many relationship
- **Django Admin**: Full admin interface for managing books and authors
- **REST API**: Complete CRUD operations for both entities
- **Advanced Queries**: Includes aggregations, annotations, and complex filtering
- **Testing**: Comprehensive unit and integration tests
- **Docker**: Fully containerized with PostgreSQL database
- **Initial Data**: Pre-loaded sample data for testing

## Technology Stack

- **Backend**: Django 4.2.9
- **API**: Django REST Framework 3.14.0
- **Database**: PostgreSQL 15
- **Containerization**: Docker & Docker Compose
- **Python**: 3.11

## Project Structure

```
drf-library-tech-challenge/
├── core/                      # Django project settings
│   ├── settings.py           # Main settings file
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI configuration
├── library/                   # Main application
│   ├── models.py             # Author and Book models
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # API viewsets with advanced queries
│   ├── admin.py              # Django admin configuration
│   ├── tests.py              # Unit and integration tests
│   └── management/
│       └── commands/
│           └── load_initial_data.py  # Initial data loader
├── Dockerfile                 # Docker image configuration
├── docker-compose.yml         # Docker Compose services
├── deploy.sh                  # Deployment script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Installation & Deployment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd drf-library-tech-challenge
   ```

2. **Run the deployment script**
   ```bash
   ./deploy.sh
   ```

3. **Follow the interactive prompts**
   - Choose option 1 for fresh deployment
   - Create a superuser when prompted
   - Optionally run tests

The deployment script will:
- Build Docker images
- Start PostgreSQL and Django containers
- Run database migrations
- Load initial sample data
- Optionally create a superuser and run tests

### Manual Deployment

If you prefer manual deployment:

```bash
# Build and start containers
docker-compose up -d --build

# Wait for database to be ready
sleep 10

# Run migrations
docker exec library_web python manage.py migrate

# Load initial data
docker exec library_web python manage.py load_initial_data

# Create superuser (optional)
docker exec -it library_web python manage.py createsuperuser

# Run tests (optional)
docker exec library_web python manage.py test
```

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### Authors

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/authors/` | List all authors |
| POST | `/api/authors/` | Create new author |
| GET | `/api/authors/{id}/` | Retrieve author details |
| PUT | `/api/authors/{id}/` | Update author |
| PATCH | `/api/authors/{id}/` | Partial update author |
| DELETE | `/api/authors/{id}/` | Delete author |
| GET | `/api/authors/{id}/books/` | Get all books by author |
| GET | `/api/authors/statistics/` | **Advanced query**: Author statistics |

### Books

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books/` | List all books |
| POST | `/api/books/` | Create new book |
| GET | `/api/books/{id}/` | Retrieve book details |
| PUT | `/api/books/{id}/` | Update book |
| PATCH | `/api/books/{id}/` | Partial update book |
| DELETE | `/api/books/{id}/` | Delete book |
| GET | `/api/books/statistics/` | **Advanced query**: Book statistics with aggregations |
| GET | `/api/books/top_rated/` | **Advanced query**: Top rated books (rating >= 4.0) |
| GET | `/api/books/recent_releases/` | **Advanced query**: Recent releases with complex filtering |
| GET | `/api/books/by_author/` | **Advanced query**: Books grouped by author count |

### Advanced Queries Examples

The application includes several advanced database queries using Django ORM's `annotate`, `aggregate`, and complex `Q` objects:

#### 1. Book Statistics (Aggregation)
```bash
GET /api/books/statistics/
```
Returns:
- Total books count
- Average, max, and min prices
- Average rating
- Total stock quantity
- Average page count
- Statistics grouped by genre
- Count of books with multiple authors

**ORM Features**: `aggregate()`, `annotate()`, `Count()`, `Avg()`, `Sum()`, `Max()`, `Min()`

#### 2. Author Statistics (Aggregation with Filters)
```bash
GET /api/authors/statistics/
```
Returns:
- Total authors
- Authors with books
- Average books per author
- Most prolific authors

**ORM Features**: `aggregate()`, `annotate()`, `Count()`, `Avg()`, `Q()` objects with filters

#### 3. Top Rated Books (Annotation + Filtering)
```bash
GET /api/books/top_rated/
```
Returns books with rating >= 4.0, annotated with author count.

**ORM Features**: `annotate()`, `Count()`, `filter()`, `order_by()`

#### 4. Recent Releases (Complex Q Objects)
```bash
GET /api/books/recent_releases/
```
Returns books from the last year that are either in stock OR highly rated.

**ORM Features**: `Q()` objects, complex filtering with `&` and `|` operators

### Query Parameters

#### Authors
- `search`: Search by name, nationality, or email
- `nationality`: Filter by nationality
- `ordering`: Sort by fields (e.g., `last_name`, `-created_at`)

Example:
```bash
GET /api/authors/?search=George&nationality=British&ordering=last_name
```

#### Books
- `search`: Search by title, ISBN, publisher, or author name
- `genre`: Filter by genre (FICTION, MYSTERY, etc.)
- `in_stock`: Filter by stock availability (true/false)
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `min_rating`: Minimum rating filter
- `ordering`: Sort by fields (e.g., `title`, `-publication_date`)

Example:
```bash
GET /api/books/?genre=FICTION&in_stock=true&min_rating=4.0&ordering=-rating
```

## Django Admin

Access the admin panel at: `http://localhost:8000/admin/`

Features:
- Create, edit, and delete books and authors
- Advanced filtering and search
- Inline editing of many-to-many relationships
- Custom list displays with computed fields

## Data Models

### Author Model
```python
- first_name: CharField
- last_name: CharField
- birth_date: DateField (optional)
- nationality: CharField
- biography: TextField
- email: EmailField (unique)
- created_at: DateTimeField (auto)
- updated_at: DateTimeField (auto)
```

### Book Model
```python
- title: CharField
- isbn: CharField (unique, validated)
- authors: ManyToManyField(Author)
- genre: CharField (choices)
- publication_date: DateField
- publisher: CharField
- page_count: PositiveIntegerField
- language: CharField
- description: TextField
- price: DecimalField
- stock_quantity: PositiveIntegerField
- rating: DecimalField (0-5)
- created_at: DateTimeField (auto)
- updated_at: DateTimeField (auto)
```

## Testing

Run the test suite:

```bash
# Run all tests
docker exec library_web python manage.py test

# Run specific test class
docker exec library_web python manage.py test library.tests.BookAPITest

# Run with verbose output
docker exec library_web python manage.py test --verbosity=2
```

Test coverage includes:
- Model validation and methods
- API CRUD operations
- Query parameter filtering
- Advanced query endpoints
- Serializer validation
- Edge cases and error handling

## Sample Data

The application comes with pre-loaded sample data including:

**Authors** (8 total):
- George Orwell
- Jane Austen
- F. Scott Fitzgerald
- Harper Lee
- J.K. Rowling
- Stephen King
- Agatha Christie
- Isaac Asimov

**Books** (10 total):
- Classic fiction, mystery, romance, science fiction, and fantasy
- Various ratings, prices, and stock levels
- Demonstrating many-to-many relationships

Reload sample data:
```bash
docker exec library_web python manage.py load_initial_data
```

## API Usage Examples

### Create an Author
```bash
curl -X POST http://localhost:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ernest",
    "last_name": "Hemingway",
    "birth_date": "1899-07-21",
    "nationality": "American",
    "email": "ernest@example.com"
  }'
```

### Create a Book
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Old Man and the Sea",
    "isbn": "0684801221",
    "author_ids": [1],
    "genre": "FICTION",
    "publication_date": "1952-09-01",
    "publisher": "Charles Scribner",
    "page_count": 127,
    "price": "14.99",
    "stock_quantity": 20,
    "rating": "4.5"
  }'
```

### Get Book Statistics
```bash
curl http://localhost:8000/api/books/statistics/
```

### Search Books
```bash
curl "http://localhost:8000/api/books/?search=Harry&in_stock=true"
```

## Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Access Django shell
docker exec -it library_web python manage.py shell

# Access database
docker exec -it library_db psql -U library_user -d library_db

# Run migrations
docker exec library_web python manage.py migrate

# Create new migration
docker exec library_web python manage.py makemigrations
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=library_db
DATABASE_USER=library_user
DATABASE_PASSWORD=library_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

## Development

### Adding New Dependencies

1. Add the package to `requirements.txt`
2. Rebuild the Docker image:
   ```bash
   docker-compose up -d --build
   ```

### Making Model Changes

1. Update models in `library/models.py`
2. Create migrations:
   ```bash
   docker exec library_web python manage.py makemigrations
   ```
3. Apply migrations:
   ```bash
   docker exec library_web python manage.py migrate
   ```

## Troubleshooting

### Database Connection Issues
```bash
# Check if database is running
docker-compose ps

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Permission Denied on deploy.sh
```bash
chmod +x deploy.sh
```

### Port Already in Use
If port 8000 or 5432 is already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8000 to another port
```

## API Documentation

For interactive API documentation, you can integrate Django REST Framework's browsable API:

Visit: `http://localhost:8000/api/`

The browsable API provides:
- Interactive forms for testing endpoints
- Automatic documentation of available endpoints
- Request/response examples

## License

This project is created as a technical challenge demonstration.

## Contact

For questions or issues, please refer to the repository's issue tracker.
