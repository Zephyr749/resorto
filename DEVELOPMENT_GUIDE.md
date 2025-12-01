# Resorto - Development Guide

## Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or Atlas)
- Git

### Initial Setup

1. **Clone and navigate:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   ```

3. **Install dependencies:**
   ```bash
   .venv/bin/pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and JWT secret
   ```

5. **Run server:**
   ```bash
   ./run.sh
   # API docs: http://localhost:8000/docs
   ```

6. **Run tests:**
   ```bash
   ./test.sh
   ```

## Project Organization

The backend is **self-contained** in the `backend/` directory:

```
backend/
├── .venv/              # Virtual environment
├── .env                # Environment variables (not committed)
├── .env.example        # Template
│
├── modules/
│   ├── auth/          # Authentication
│   │   ├── auth_controller.py    # API endpoints
│   │   ├── auth_service.py       # Business logic
│   │   └── auth_repo.py          # Database operations
│   │
│   ├── booking/       # Booking system
│   │   ├── booking_service.py    # Business logic
│   │   └── booking_repo.py       # Database operations
│   │
│   ├── common/        # Shared utilities
│   │   ├── auth_middleware.py    # JWT verification
│   │   ├── admin_middleware.py   # Admin role check
│   │   ├── utils.py              # Helper functions
│   │   ├── logger.py             # Logging
│   │   └── config.py             # Configuration
│   │
│   └── db/            # Database
│       ├── mongo_client.py       # MongoDB connection
│       ├── schemas.py            # User schemas
│       └── booking_schemas.py    # Booking schemas
│
├── tests/             # Test suite
│   ├── conftest.py              # Fixtures
│   ├── test_api.py              # API tests
│   ├── test_auth_service.py    # Service tests
│   ├── test_auth_repo.py       # Repository tests
│   └── test_utils.py            # Utility tests
│
├── main.py            # FastAPI application
├── requirements.txt   # Dependencies
├── pytest.ini        # Test configuration
├── run.sh            # Start script
└── test.sh           # Test script
```

## Architecture

### Layered Architecture

```
Controller → Service → Repository → Database
```

- **Controller:** HTTP endpoints, request/response handling
- **Service:** Business logic, validation, authorization
- **Repository:** Database operations, queries
- **Schemas:** Pydantic models for validation

### Example Flow

```python
# 1. Controller (auth_controller.py)
@router.post('/login')
def login(credentials: Credentials, response: Response):
    result = loginUser(credentials)  # Call service
    return build_response(True, result, 'Login successful')

# 2. Service (auth_service.py)
def loginUser(credentials: Credentials) -> LoginResponse:
    user = repository.getUserByEmail(email)  # Call repository
    # Business logic: verify password, create token
    return LoginResponse(user=user_obj, token=token)

# 3. Repository (auth_repo.py)
def getUserByEmail(self, email: str) -> Optional[dict]:
    return self.users.find_one({'email': email})  # Database query
```

## HTTP Status Codes

The API uses proper HTTP status codes with consistent response structure:

### Success (200)
```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful"
}
```

### Errors
- **400 Bad Request:** Validation errors, invalid input
- **401 Unauthorized:** Authentication failed (wrong password)
- **403 Forbidden:** Insufficient permissions (not admin)
- **404 Not Found:** Resource doesn't exist
- **409 Conflict:** Business rule violation (spot not available)
- **500 Internal Server Error:** Server errors

```json
{
  "success": false,
  "error": "Error description",
  "message": "Operation failed"
}
```

## Authentication

### JWT Token Flow

1. User logs in with email/password
2. Server verifies credentials
3. Server generates JWT token (valid 24 hours)
4. Client stores token
5. Client sends token in `Authorization` header
6. Middleware verifies token for protected routes

### Protected Routes

```python
# Requires authentication
@router.get('/profile')
def getProfile(user_id: str = Depends(get_current_user_id)):
    return getUserProfile(user_id)

# Requires admin role
@router.post('/admin/spots')
def createSpot(spot: SpotCreate, admin_id: str = Depends(require_admin)):
    return createSpot(spot)
```

## Testing

### Test Structure

- **Unit Tests:** Test individual functions in isolation
- **Integration Tests:** Test API endpoints end-to-end
- **Fixtures:** Shared test data and setup

### Running Tests

```bash
# All tests
./test.sh

# Specific file
.venv/bin/python -m pytest tests/test_api.py -v

# With coverage
.venv/bin/python -m pytest tests/ --cov=modules

# Quiet mode
.venv/bin/python -m pytest tests/ -q
```

### Writing Tests

```python
# conftest.py provides fixtures
def test_login_success(client, sample_user):
    response = client.post('/auth/login', json={
        'email': sample_user['email'],
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'token' in data['data']
```

## Environment Variables

Create `.env` file in backend directory:

```bash
# MongoDB
MONGODB_URI=mongodb://localhost:27017
DB_NAME=resorto

# JWT
JWT_SECRET=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Razorpay (when implemented)
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

## Database

### MongoDB Collections

**users:**
- `_id`: ObjectId
- `email`: string (unique)
- `password`: string (bcrypt hashed)
- `firstName`: string
- `lastName`: string
- `role`: "user" | "admin"

**spots:**
- `_id`: ObjectId
- `name`: string
- `description`: string
- `spotType`: "picnic_area" | "room"
- `capacity`: number
- `pricePerDay`: number
- `amenities`: string[]
- `images`: string[]
- `isActive`: boolean
- `createdAt`: Date
- `updatedAt`: Date

**bookings:**
- `_id`: ObjectId
- `userId`: string
- `spotId`: string
- `checkInDate`: Date
- `checkOutDate`: Date
- `numberOfGuests`: number
- `specialRequests`: string
- `status`: "pending" | "confirmed" | "cancelled" | "completed"
- `totalAmount`: number
- `paymentStatus`: "pending" | "paid" | "failed" | "refunded"
- `paymentId`: string
- `createdAt`: Date
- `updatedAt`: Date

## Common Tasks

### Add a New Endpoint

1. **Define schema** in `modules/db/schemas.py`:
   ```python
   class NewFeature(BaseModel):
       name: str
       value: int
   ```

2. **Add repository method** in appropriate `_repo.py`:
   ```python
   def createFeature(self, data: dict) -> str:
       result = self.collection.insert_one(data)
       return str(result.inserted_id)
   ```

3. **Add service method** in appropriate `_service.py`:
   ```python
   def createFeature(data: NewFeature) -> dict:
       feature_id = repository.createFeature(data.dict())
       return {'id': feature_id}
   ```

4. **Add controller endpoint** in appropriate `_controller.py`:
   ```python
   @router.post('/features')
   def create_feature(data: NewFeature):
       result = createFeature(data)
       return build_response(True, result, 'Created')
   ```

5. **Register router** in `main.py`:
   ```python
   app.include_router(feature_controller.router)
   ```

6. **Write tests** in `tests/test_features.py`

### Add a New Middleware

1. Create file in `modules/common/`:
   ```python
   def my_middleware(header: str = Header(None)):
       if not header:
           raise HTTPException(status_code=400, detail='Missing header')
       return header
   ```

2. Use in endpoint:
   ```python
   @router.get('/endpoint')
   def endpoint(value: str = Depends(my_middleware)):
       return {'value': value}
   ```

### Debug Issues

1. **Check logs:** Look at console output
2. **Use API docs:** http://localhost:8000/docs for testing
3. **Run specific test:** `pytest tests/test_file.py::test_name -v`
4. **Check database:** Use MongoDB Compass or mongosh
5. **Print debugging:** Use `logger.info()` or `print()`

## Coding Conventions

### Style
- Follow PEP 8
- Use type hints
- Keep functions small and focused
- Use meaningful variable names

### Naming
- **Files:** `snake_case.py`
- **Classes:** `PascalCase`
- **Functions:** `camelCase` (for consistency with existing code)
- **Variables:** `camelCase`
- **Constants:** `UPPER_CASE`

### Imports
```python
# Standard library
from datetime import datetime
from typing import List, Optional

# Third-party
from fastapi import APIRouter, Depends
from pydantic import BaseModel

# Local
from modules.common.utils import build_response
from modules.db.schemas import User
```

### Error Handling
```python
try:
    result = some_operation()
    return build_response(True, result, 'Success')
except HTTPException as he:
    response.status_code = he.status_code
    return build_response(False, str(he.detail), 'Failed')
except Exception as e:
    logger.error(f'Error: {e}')
    response.status_code = 500
    return build_response(False, str(e), 'Server error')
```

## Deployment

### Preparation
1. Update `.env` with production values
2. Set `JWT_SECRET` to strong random value
3. Use MongoDB Atlas for production database
4. Set proper CORS origins in `main.py`

### Running in Production
```bash
cd backend
.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Using Process Manager (PM2)
```bash
pm2 start ".venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000" --name resorto-api
```

## Troubleshooting

### Tests Failing
- Ensure MongoDB is running
- Check `.env` configuration
- Run `pytest tests/ -v` for detailed output
- Clear `__pycache__` directories

### Import Errors
- Ensure you're in backend directory
- Activate virtual environment
- Reinstall dependencies: `.venv/bin/pip install -r requirements.txt`

### Database Connection Issues
- Check MongoDB is running: `mongosh`
- Verify `MONGODB_URI` in `.env`
- Check network connectivity

### Authentication Issues
- Verify JWT_SECRET is set
- Check token expiration
- Ensure Authorization header format: `Bearer <token>`

## Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **MongoDB Docs:** https://docs.mongodb.com/
- **Pydantic Docs:** https://docs.pydantic.dev/
- **pytest Docs:** https://docs.pytest.org/

---

**Happy Coding! 🚀**
