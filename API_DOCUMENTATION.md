# API Documentation

This document provides comprehensive information about the Riget Zoo Adventures API endpoints, data models, and usage examples.

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [Base URL](#base-url)
- [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

## Overview

The Riget Zoo Adventures API provides access to zoo information, booking functionality, event management, and user authentication. The API follows RESTful principles and returns JSON responses.

### API Features
- User authentication and registration
- Booking management
- Event information
- Opening hours and calendar data
- User validation endpoints

## Authentication

The API uses Django's built-in authentication system with session-based authentication for web interface and token authentication for API access.

### Authentication Methods
1. **Session Authentication** (Web Interface)
2. **Token Authentication** (API Access)
3. **Email or Username Login** (Custom Backend)

### Login Endpoint
```http
POST /login/
Content-Type: application/json

{
    "username": "user@example.com",  // Email or username
    "password": "your_password"
}
```

## Base URL

- **Development**: `http://127.0.0.1:8000/`
- **Production**: `https://your-domain.com/` (Update with actual domain)

## Data Models

### User Model
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "12345678901",
    "is_active": true,
    "date_joined": "2025-10-02T10:00:00Z"
}
```

### Booking Model
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "12345678901",
    "booking_date": "2025-10-15",
    "booking_time": "10:00:00",
    "message": "Family visit with 2 children"
}
```

### Event Model
```json
{
    "id": 1,
    "title": "Lion Feeding Time",
    "start_time": "2025-10-15T14:00:00Z",
    "end_time": "2025-10-15T14:30:00Z",
    "description": "Watch our majestic lions during feeding time",
    "location": "Lion Enclosure",
    "created_at": "2025-10-02T10:00:00Z",
    "updated_at": "2025-10-02T10:00:00Z"
}
```

### Opening Hours Model
```json
{
    "id": 1,
    "date": "2025-10-15",
    "opening_time": "09:00",
    "closing_time": "18:00",
    "color": "purple"
}
```

### Closed Days Model
```json
{
    "id": 1,
    "date": "2025-12-25",
    "reason": "Christmas Day"
}
```

## API Endpoints

### Authentication Endpoints

#### User Registration
```http
POST /signup/
Content-Type: application/json

{
    "username": "new_user",
    "email": "newuser@example.com",
    "password1": "secure_password123",
    "password2": "secure_password123",
    "phone_number": "12345678901"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "User created successfully",
    "user_id": 123
}
```

#### User Login
```http
POST /login/
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "your_password"
}
```

#### User Logout
```http
POST /logout/
```

#### Check User Exists
```http
POST /check_user_exists/
Content-Type: application/json

{
    "username": "john_doe"
}
```

**Response:**
```json
{
    "exists": true,
    "user_id": 123
}
```

#### Validate User Password
```http
POST /check_user_exists_password/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "user_password"
}
```

### Booking Endpoints

#### Create Booking
```http
POST /booking/
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "12345678901",
    "booking_date": "2025-10-15",
    "booking_time": "10:00",
    "message": "Family visit with 2 children"
}
```

**Response:**
```json
{
    "status": "success",
    "booking_id": 456,
    "message": "Booking created successfully"
}
```

#### Get Booking Success
```http
GET /booking/success/
```

### Calendar and Hours Endpoints

#### Get Calendar Data
```http
GET /calendar-data/
GET /calendar-data/?year=2025&month=10
```

**Response:**
```json
{
    "year": 2025,
    "month": 10,
    "days": [
        {
            "date": "2025-10-01",
            "opening_time": "09:00",
            "closing_time": "18:00",
            "color": "purple",
            "is_closed": false
        },
        {
            "date": "2025-10-02",
            "is_closed": true,
            "reason": "Maintenance Day"
        }
    ]
}
```

#### Get Day Details
```http
GET /get-day-details/?date=2025-10-15
```

**Response:**
```json
{
    "date": "2025-10-15",
    "opening_time": "09:00",
    "closing_time": "18:00",
    "is_closed": false,
    "events": [
        {
            "title": "Lion Feeding",
            "time": "14:00",
            "location": "Lion Enclosure"
        }
    ]
}
```

### Page Endpoints (Static Content)

#### Homepage
```http
GET /
```

#### About Us
```http
GET /aboutus
```

#### Animals
```http
GET /animals
```

#### Events
```http
GET /events
```

#### Conservation
```http
GET /conservation
```

#### Visit Information
```http
GET /visit
```

## Error Handling

### Standard Error Response Format
```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "field_name": ["Error message for this field"]
        }
    }
}
```

### Common HTTP Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### Error Code Examples

#### Validation Errors
```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Phone number must be at least 11 digits long",
        "field": "phone_number"
    }
}
```

#### Authentication Errors
```json
{
    "error": {
        "code": "AUTHENTICATION_ERROR",
        "message": "Invalid credentials"
    }
}
```

#### Resource Not Found
```json
{
    "error": {
        "code": "NOT_FOUND",
        "message": "Booking not found"
    }
}
```

## Rate Limiting

Currently, there are no explicit rate limits implemented, but it's recommended to:
- Limit requests to 100 per minute per IP
- Implement authentication-based rate limiting for logged-in users
- Use caching for frequently accessed data

## Examples

### Complete Booking Flow

#### 1. Check if date is available
```bash
curl -X GET "http://127.0.0.1:8000/get-day-details/?date=2025-10-15" \
     -H "Content-Type: application/json"
```

#### 2. Create a booking
```bash
curl -X POST http://127.0.0.1:8000/booking/ \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "phone": "12345678901",
       "booking_date": "2025-10-15",
       "booking_time": "10:00",
       "message": "Family visit"
     }'
```

### User Registration and Login

#### 1. Register a new user
```bash
curl -X POST http://127.0.0.1:8000/signup/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "email": "newuser@example.com",
       "password1": "securepass123",
       "password2": "securepass123",
       "phone_number": "12345678901"
     }'
```

#### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/login/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser@example.com",
       "password": "securepass123"
     }'
```

### Calendar Integration

#### Get current month calendar
```bash
curl -X GET "http://127.0.0.1:8000/calendar-data/" \
     -H "Content-Type: application/json"
```

#### Get specific month
```bash
curl -X GET "http://127.0.0.1:8000/calendar-data/?year=2025&month=12" \
     -H "Content-Type: application/json"
```

## Frontend Integration

### JavaScript Example
```javascript
// Booking creation example
async function createBooking(bookingData) {
    try {
        const response = await fetch('/booking/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Django CSRF token
            },
            body: JSON.stringify(bookingData)
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Booking created:', result);
            window.location.href = '/booking/success/';
        } else {
            const error = await response.json();
            console.error('Booking error:', error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

// Get CSRF token function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

## Development Notes

### Adding New Endpoints
1. Define URL patterns in `urls.py`
2. Create view functions in `views.py`
3. Add proper error handling
4. Update this documentation
5. Add tests for new endpoints

### API Versioning
Currently, the API doesn't use versioning. For future versions, consider:
- URL versioning: `/api/v1/bookings/`
- Header versioning: `Accept: application/vnd.api+json;version=1`

### Future Enhancements
- REST API with Django REST Framework
- OpenAPI/Swagger documentation
- Pagination for list endpoints
- Filtering and searching capabilities
- Webhook support for booking notifications
- Mobile app API endpoints

---

**Last Updated**: October 2025

For support or questions about the API, please refer to our [Contributing Guidelines](CONTRIBUTING.md) or open an issue on GitHub.