# Car Rental System Backend

This repository contains the backend implementation for a Car Rental System built with FastAPI, SQLModel, and PostgreSQL.

## Project Analysis

The application provides a comprehensive platform for car rentals including user authentication, vehicle management, booking systems with conflict detection, and a transaction-based payment tracking system with refund support.

### Key Features

1. User Authentication: Robust signup and login system using JWT tokens and HTTP Bearer authorization.
2. Vehicle Management: Detailed vehicle listings with real-time availability status.
3. Booking System: Preventive logic for overlapping bookings, maximum booking duration of 7 days, and restriction on past-date bookings.
4. Transactional Payments: Detailed payment tracking including transaction IDs, vehicle references, and automated refund status updates upon cancellation.
5. KYC Verification: Email-verified KYC system to ensure secure user onboarding.

## Folder Structure

```
.
├── alembic                      # Database migration configuration and history
│   ├── versions                 # Migration files
│   └── env.py                   # Alembic environment setup
├── app                          # Main application directory
│   ├── api                      # Dependency injection and utilities
│   ├── core                     # Core configurations (database, security, redis, email)
│   ├── models                   # SQLModel database schemas
│   ├── repositories             # Database interaction layer (CRUD)
│   ├── routers                  # API route definitions
│   ├── schemas                  # Pydantic request/response schemas
│   ├── services                 # Business logic layer
│   └── main.py                  # Entry point for the FastAPI application
├── .env                         # Environment variables (Real)
├── .env.example                 # Example environment variables
├── alembic.ini                  # Alembic configuration
└── requirements.txt             # Project dependencies
```

## API Routes

The following routes are available in the application:

### Authentication (Auth)

- POST /auth/signup: Create a new user account.
- POST /auth/login: Authenticate user and receive access token.

### User Management (Users)

- GET /users/me: Retrieve current logged-in user profile.
- PUT /users/me: Update current user profile.

### Vehicle Management (Vehicles)

- GET /vehicles/: List all active vehicles with their current availability status.
- POST /vehicles/: Create a new vehicle (Admin only).

### Booking Management (Bookings)

- POST /bookings/: Create a new vehicle booking.
- POST /bookings/cancel/{booking_id}: Cancel an existing booking and trigger refund.
- GET /bookings/me: View booking history for the current user.

### KYC Management (KYC)

- POST /kyc/submit: Submit KYC documents (Email must match account email).
- POST /kyc/verify: Verify KYC using OTP sent to email.

### Admin Operations (Admin)

- POST /admin/vehicles/: Admin endpoint to create vehicles.
- DELETE /admin/vehicles/{vehicle_id}: Remove a vehicle from the system.
- GET /admin/vehicles/: List all vehicles with detailed booking history and status.

## Configuration

The application requires specific environment variables to be set in a .env file. Reference the .env.example file for the required keys.

- DATABASE_URL: PostgreSQL connection string.
- SECRET_KEY: Used for JWT token signing.
- REDIS_URL: Upstash Redis connection string for OTP/caching.
- SMTP Settings: Required for email verification and KYC notifications.

## Database Migrations

Database schema changes are managed using Alembic. To apply migrations:

```bash
alembic upgrade head
```
