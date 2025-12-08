#!/bin/bash

# Library Management System - Deployment Script
# This script handles the deployment of the Django REST Framework application

set -e  # Exit on error

echo "======================================"
echo "Library Management System Deployment"
echo "======================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_info "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_info "Docker is installed: $(docker --version)"
}

# Check if Docker Compose is installed
check_docker_compose() {
    print_info "Checking Docker Compose installation..."
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    if command -v docker-compose &> /dev/null; then
        print_info "Docker Compose is installed: $(docker-compose --version)"
    else
        print_info "Docker Compose is installed: $(docker compose version)"
    fi
}

# Function to determine docker-compose command
get_compose_cmd() {
    if command -v docker-compose &> /dev/null; then
        echo "docker-compose"
    else
        echo "docker compose"
    fi
}

# Stop and remove existing containers
cleanup() {
    print_info "Cleaning up existing containers..."
    COMPOSE_CMD=$(get_compose_cmd)
    $COMPOSE_CMD down -v || true
    print_info "Cleanup completed"
}

# Build Docker images
build_images() {
    print_info "Building Docker images..."
    COMPOSE_CMD=$(get_compose_cmd)
    $COMPOSE_CMD build
    print_info "Docker images built successfully"
}

# Start services
start_services() {
    print_info "Starting services..."
    COMPOSE_CMD=$(get_compose_cmd)
    $COMPOSE_CMD up -d
    print_info "Services started successfully"
}

# Wait for database to be ready
wait_for_db() {
    print_info "Waiting for database to be ready..."
    sleep 5

    max_attempts=30
    attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if docker exec library_db pg_isready -U library_user -d library_db &> /dev/null; then
            print_info "Database is ready!"
            return 0
        fi
        attempt=$((attempt + 1))
        echo "Waiting for database... (attempt $attempt/$max_attempts)"
        sleep 2
    done

    print_error "Database failed to start within the expected time"
    exit 1
}

# Run migrations
run_migrations() {
    print_info "Running database migrations..."
    docker exec library_web python manage.py migrate
    print_info "Migrations completed successfully"
}

# Create superuser
create_superuser() {
    print_info "Creating Django superuser..."
    print_warning "You will be prompted to enter superuser credentials"
    docker exec -it library_web python manage.py createsuperuser || true
}

# Load initial data
load_initial_data() {
    print_info "Loading initial data..."
    docker exec library_web python manage.py load_initial_data
    print_info "Initial data loaded successfully"
}

# Run tests
run_tests() {
    print_info "Running tests..."
    docker exec library_web python manage.py test
    print_info "All tests passed!"
}

# Display service information
display_info() {
    echo ""
    echo "======================================"
    echo "Deployment Completed Successfully!"
    echo "======================================"
    echo ""
    print_info "Services are running:"
    echo ""
    echo "  📚 API Documentation: http://localhost:8000/api/"
    echo "  🔧 Django Admin:      http://localhost:8000/admin/"
    echo "  📖 Books API:         http://localhost:8000/api/books/"
    echo "  👤 Authors API:       http://localhost:8000/api/authors/"
    echo ""
    print_info "API Endpoints with advanced queries:"
    echo "  - GET /api/books/statistics/       - Book statistics with aggregations"
    echo "  - GET /api/books/top_rated/        - Top rated books"
    echo "  - GET /api/books/recent_releases/  - Recent releases"
    echo "  - GET /api/authors/statistics/     - Author statistics"
    echo ""
    print_info "Useful commands:"
    echo "  - View logs:        $(get_compose_cmd) logs -f"
    echo "  - Stop services:    $(get_compose_cmd) down"
    echo "  - Restart services: $(get_compose_cmd) restart"
    echo "  - Run tests:        docker exec library_web python manage.py test"
    echo ""
}

# Main deployment flow
main() {
    check_docker
    check_docker_compose

    # Ask user what to do
    echo ""
    echo "Deployment Options:"
    echo "1) Fresh deployment (clean install)"
    echo "2) Quick start (use existing containers)"
    echo "3) Run tests only"
    echo "4) Stop all services"
    echo ""
    read -p "Enter your choice (1-4): " choice

    case $choice in
        1)
            print_info "Starting fresh deployment..."
            cleanup
            build_images
            start_services
            wait_for_db
            run_migrations
            load_initial_data
            echo ""
            read -p "Do you want to create a superuser? (y/n): " create_super
            if [ "$create_super" = "y" ] || [ "$create_super" = "Y" ]; then
                create_superuser
            fi
            echo ""
            read -p "Do you want to run tests? (y/n): " run_test
            if [ "$run_test" = "y" ] || [ "$run_test" = "Y" ]; then
                run_tests
            fi
            display_info
            ;;
        2)
            print_info "Starting quick deployment..."
            start_services
            wait_for_db
            display_info
            ;;
        3)
            print_info "Running tests..."
            run_tests
            ;;
        4)
            print_info "Stopping all services..."
            cleanup
            print_info "All services stopped"
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
}

# Run main function
main
