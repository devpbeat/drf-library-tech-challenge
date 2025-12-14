"""
Custom exception handling for the Library API.
Provides consistent error responses across all endpoints.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    MethodNotAllowed,
    ValidationError,
    Throttled,
    ParseError,
)
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error response format.
    
    Response format:
    {
        "success": false,
        "error": {
            "code": "ERROR_CODE",
            "message": "Human readable message",
            "details": {} or []  # Optional additional details
        }
    }
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Get request info for logging
    request = context.get('request')
    view = context.get('view')
    
    # Build error response
    error_response = {
        'success': False,
        'error': {
            'code': 'UNKNOWN_ERROR',
            'message': 'An unexpected error occurred.',
            'details': None
        }
    }
    
    if response is not None:
        # Handle DRF exceptions
        error_response['error'] = _handle_drf_exception(exc, response)
        response.data = error_response
        
    else:
        # Handle non-DRF exceptions
        response = _handle_non_drf_exception(exc, error_response)
    
    # Log the exception
    _log_exception(exc, request, view)
    
    return response


def _handle_drf_exception(exc, response):
    """Handle Django REST Framework exceptions."""
    
    error_data = {
        'code': 'UNKNOWN_ERROR',
        'message': 'An error occurred.',
        'details': None
    }
    
    if isinstance(exc, ValidationError):
        error_data['code'] = 'VALIDATION_ERROR'
        error_data['message'] = 'The provided data is invalid.'
        error_data['details'] = response.data
        
    elif isinstance(exc, AuthenticationFailed):
        error_data['code'] = 'AUTHENTICATION_FAILED'
        # Handle JWT specific errors
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                error_data['message'] = str(exc.detail.get('detail', 'Authentication failed.'))
            else:
                error_data['message'] = str(exc.detail)
        else:
            error_data['message'] = 'Authentication failed.'
        
    elif isinstance(exc, NotAuthenticated):
        error_data['code'] = 'NOT_AUTHENTICATED'
        error_data['message'] = 'Authentication credentials were not provided.'
        
    elif isinstance(exc, PermissionDenied):
        error_data['code'] = 'PERMISSION_DENIED'
        error_data['message'] = str(exc.detail) if hasattr(exc, 'detail') else 'You do not have permission to perform this action.'
        
    elif isinstance(exc, NotFound):
        error_data['code'] = 'NOT_FOUND'
        error_data['message'] = str(exc.detail) if hasattr(exc, 'detail') else 'The requested resource was not found.'
        
    elif isinstance(exc, MethodNotAllowed):
        error_data['code'] = 'METHOD_NOT_ALLOWED'
        error_data['message'] = str(exc.detail) if hasattr(exc, 'detail') else 'Method not allowed for this endpoint.'
        
    elif isinstance(exc, Throttled):
        error_data['code'] = 'THROTTLED'
        error_data['message'] = f'Request was throttled. Please wait {exc.wait} seconds.'
        error_data['details'] = {'retry_after': exc.wait}
        
    elif isinstance(exc, ParseError):
        error_data['code'] = 'PARSE_ERROR'
        error_data['message'] = 'Malformed request. Could not parse the request body.'
        
    elif isinstance(exc, APIException):
        error_data['code'] = exc.default_code.upper() if hasattr(exc, 'default_code') else 'API_ERROR'
        error_data['message'] = str(exc.detail) if hasattr(exc, 'detail') else str(exc)
    
    # Handle 404 responses that weren't caught by NotFound
    if response.status_code == 404 and error_data['code'] == 'UNKNOWN_ERROR':
        error_data['code'] = 'NOT_FOUND'
        error_data['message'] = 'The requested resource was not found.'
        
    return error_data


def _handle_non_drf_exception(exc, error_response):
    """Handle exceptions not caught by DRF's default handler."""
    
    if isinstance(exc, Http404) or isinstance(exc, ObjectDoesNotExist):
        error_response['error']['code'] = 'NOT_FOUND'
        error_response['error']['message'] = 'The requested resource was not found.'
        return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        
    elif isinstance(exc, DjangoPermissionDenied):
        error_response['error']['code'] = 'PERMISSION_DENIED'
        error_response['error']['message'] = 'You do not have permission to perform this action.'
        return Response(error_response, status=status.HTTP_403_FORBIDDEN)
        
    elif isinstance(exc, IntegrityError):
        error_response['error']['code'] = 'INTEGRITY_ERROR'
        error_response['error']['message'] = 'Database integrity error. This may be due to duplicate data or invalid references.'
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        # Unknown exception - return 500
        error_response['error']['code'] = 'INTERNAL_SERVER_ERROR'
        error_response['error']['message'] = 'An internal server error occurred. Please try again later.'
        return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _log_exception(exc, request, view):
    """Log exception details for debugging."""
    
    view_name = view.__class__.__name__ if view else 'Unknown'
    method = request.method if request else 'Unknown'
    path = request.path if request else 'Unknown'
    
    logger.error(
        f"Exception in {view_name} [{method} {path}]: {exc.__class__.__name__}: {str(exc)}",
        exc_info=True,
        extra={
            'view': view_name,
            'method': method,
            'path': path,
        }
    )


# Custom API Exceptions for specific use cases

class BadRequest(APIException):
    """Exception for general bad request errors."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request.'
    default_code = 'bad_request'


class Conflict(APIException):
    """Exception for resource conflicts (e.g., duplicate entries)."""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resource conflict.'
    default_code = 'conflict'


class Gone(APIException):
    """Exception for resources that no longer exist."""
    status_code = status.HTTP_410_GONE
    default_detail = 'Resource no longer available.'
    default_code = 'gone'


class UnprocessableEntity(APIException):
    """Exception for semantically incorrect requests."""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Unprocessable entity.'
    default_code = 'unprocessable_entity'


class ServiceUnavailable(APIException):
    """Exception for temporary service unavailability."""
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service temporarily unavailable.'
    default_code = 'service_unavailable'


class BookNotAvailable(APIException):
    """Exception when a book is not in stock."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This book is currently not available.'
    default_code = 'book_not_available'


class AuthorHasBooks(APIException):
    """Exception when trying to delete an author who has books."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Cannot delete author with associated books.'
    default_code = 'author_has_books'


class InvalidISBN(APIException):
    """Exception for invalid ISBN format."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid ISBN format.'
    default_code = 'invalid_isbn'


class DuplicateISBN(APIException):
    """Exception for duplicate ISBN."""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'A book with this ISBN already exists.'
    default_code = 'duplicate_isbn'
