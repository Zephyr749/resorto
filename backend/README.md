# Resorto Backend

A FastAPI-based RESTful API for user authentication and profile management with complete test coverage.

## Features

- **User Authentication**
  - User registration with email validation
  - Secure login with JWT tokens
  - Password validation (min 8 chars, uppercase, lowercase, number, special character)
  
- **Profile Management**
  - Get user profile
  - Update user profile
  - Change password with current password verification

- **Security**
  - Password hashing with bcrypt
  - JWT-based authentication
  - Protected routes with token verification

- **Testing**
  - 100% test coverage
  - Unit tests for all functions
  - Integration tests for all API endpoints
  - In-memory MongoDB for isolated testing

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB
- **Authentication**: JWT (pyjwt)
- **Password Hashing**: bcrypt
- **Testing**: pytest, mongomock, httpx
- **Validation**: Pydantic

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── modules/
│   ├── auth/              # Authentication module
│   │   ├── auth_controller.py  # API endpoints
│   │   ├── auth_service.py     # Business logic
│   │   └── auth_repo.py        # Database operations
│   ├── common/            # Shared utilities
│   │   ├── config.py          # Configuration management
│   │   ├── auth_middleware.py # JWT verification
│   │   ├── utils.py           # Helper functions
│   │   └── logger.py          # Logging configuration
│   └── db/                # Database module
│       ├── mongo_client.py    # MongoDB connection
│       └── schemas.py         # Pydantic models
├── tests/                 # Test suite
│   ├── conftest.py           # Test configuration
│   ├── test_auth_service.py  # Service tests
│   ├── test_auth_repo.py     # Repository tests
│   ├── test_utils.py         # Utility tests
│   └── test_api.py           # API integration tests
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── .env.example          # Environment variables template
└── Resorto.postman_collection.json  # Postman collection

```

## Getting Started

### Prerequisites

- Python 3.13+
- MongoDB instance (local or cloud)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   MONGODB_URI=mongodb://localhost:27017
   DB_NAME=resorto
   JWT_SECRET=your-secret-key-change-this-in-production
   JWT_EXPIRATION_DAYS=7
   ```

### Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

### Running Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Run with coverage:**
```bash
pytest tests/ -v --cov=modules --cov-report=html
```

**Run specific test file:**
```bash
pytest tests/test_auth_service.py -v
```

**Run specific test:**
```bash
pytest tests/test_auth_service.py::TestAuthService::test_register_user_success -v
```

## API Endpoints

### Authentication

#### POST `/auth/register`
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "...",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "fullName": "John Doe"
    },
    "token": "eyJ..."
  },
  "message": "User registered successfully"
}
```

#### POST `/auth/login`
Login with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {...},
    "token": "eyJ..."
  },
  "message": "Login successful"
}
```

### Profile Management (Protected Routes)

All profile endpoints require `Authorization: Bearer <token>` header.

#### GET `/auth/profile`
Get current user's profile.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "fullName": "John Doe"
  },
  "message": "Profile retrieved successfully"
}
```

#### PUT `/auth/profile`
Update user profile.

**Request Body:**
```json
{
  "firstName": "Jane",
  "lastName": "Smith"
}
```

#### POST `/auth/change-password`
Change user password.

**Request Body:**
```json
{
  "currentPassword": "SecurePass123!",
  "newPassword": "NewSecurePass123!"
}
```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (!@#$%^&*(),.?":{}|<>)

## Postman Collection

Import `Resorto.postman_collection.json` into Postman for easy API testing.

**Features:**
- Auto-saves JWT token after login/register
- Pre-configured requests for all endpoints
- Environment variables for easy configuration

**Setup:**
1. Import the collection
2. Update `baseUrl` variable if needed (default: http://localhost:8000)
3. Use "Register User" or "Login" to get authenticated
4. Token is automatically added to protected routes

## Testing Strategy

### Unit Tests
- **Service Layer**: Tests business logic in isolation
- **Repository Layer**: Tests database operations with mongomock
- **Utilities**: Tests validators, password helpers, response builders

### Integration Tests
- **API Tests**: End-to-end testing of all endpoints
- **Authentication Flow**: Register → Login → Protected routes
- **Error Handling**: Invalid inputs, missing tokens, wrong passwords

### Test Coverage
- All authentication flows
- Profile management operations
- Password change functionality
- Input validation
- Error scenarios
- JWT token verification

## Development

### Code Structure
- **Controllers**: Handle HTTP requests/responses
- **Services**: Implement business logic
- **Repositories**: Handle database operations
- **Models/Schemas**: Define data structures
- **Utilities**: Shared helper functions

### Adding New Endpoints

1. **Define schema** in `modules/db/schemas.py`
2. **Add repository method** in respective repo file
3. **Implement service logic** in service file
4. **Create controller endpoint** in controller file
5. **Add route** to main.py
6. **Write tests** in tests directory

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Ensure all tests pass
5. Submit a pull request
