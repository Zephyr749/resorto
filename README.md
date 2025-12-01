# Resorto - Resort Management System

A complete resort management system for picnic spots and accommodations, built with FastAPI (backend) and React + TypeScript + Vite (frontend - coming soon).

## Project Status

### ✅ **Step 1: Backend Foundation - COMPLETED**

The backend foundation is fully built, tested, and ready for use:

- ✅ **User Authentication System**
  - User registration with comprehensive validation
  - Secure login with JWT tokens
  - Password management (change password)
  - Profile management (get/update)

- ✅ **Security Features**
  - Password hashing with bcrypt
  - JWT-based authentication middleware
  - Protected routes
  - Email validation
  - Strong password requirements

- ✅ **Complete Test Suite**
  - **51 tests** - 100% passing
  - Unit tests for all functions
  - Integration tests for all API endpoints
  - In-memory MongoDB for isolated testing
  - **Test coverage**: Service layer, Repository layer, API layer, Utilities

- ✅ **Developer Tools**
  - Postman collection with auto-token management
  - Environment configuration (.env.example)
  - Run scripts for easy startup
  - Test scripts
  - Comprehensive documentation

### 🔄 **Step 2: Resort Management Features - PENDING**

The following features will be added next:
- Booking system for resort spots and rooms
- Payment integration (Razorpay)
- Admin dashboard
- Image management
- Availability calendar
- Booking management

### 🔄 **Frontend - PENDING**

React + TypeScript + Vite frontend will be built with:
- Modern UI with Ant Design
- Authentication pages
- Profile management
- Booking interface
- Admin dashboard

## 🚀 Quick Start (Single Command!)

### Start Everything
```bash
./start.sh
```

This single command starts both backend and frontend!

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Stop:**
```bash
./stop.sh
```

Or press Ctrl+C

---

## 📋 Quick Start (Detailed)

### Backend

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and JWT secret
   ```

4. **Run the application**
   ```bash
   ./run.sh
   # Or: uvicorn main:app --reload
   ```

5. **Run tests**
   ```bash
   ./test.sh
   # Or: pytest tests/ -v
   ```

6. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Project Structure

```
Resorto/
├── backend/                    # FastAPI backend (READY)
│   ├── modules/
│   │   ├── auth/              # Authentication module
│   │   ├── common/            # Shared utilities
│   │   └── db/                # Database module
│   ├── tests/                 # Complete test suite (51 tests)
│   ├── main.py                # Application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── pytest.ini            # Test configuration
│   ├── .env.example          # Environment template
│   ├── run.sh                # Start script
│   ├── test.sh               # Test script
│   ├── README.md             # Backend documentation
│   └── Resorto.postman_collection.json
│
├── frontend/                  # React frontend (COMING SOON)
└── README.md                 # This file
```

## Technology Stack

### Backend (Current)
- **Framework**: FastAPI
- **Database**: MongoDB
- **Authentication**: JWT (pyjwt)
- **Password Hashing**: bcrypt
- **Testing**: pytest, mongomock, httpx
- **Validation**: Pydantic

### Frontend (Planned)
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **UI Library**: Ant Design
- **State Management**: Context API / Zustand
- **HTTP Client**: Axios
- **Routing**: React Router

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

### Profile Management (Protected)
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update profile
- `POST /auth/change-password` - Change password

See `backend/README.md` for detailed API documentation.

## Testing

The backend has complete test coverage with 51 tests:

```bash
cd backend
pytest tests/ -v
```

**Test Results:**
```
51 passed in 6.13s
```

**Test Categories:**
- 15 API integration tests
- 7 Repository tests
- 12 Service layer tests
- 17 Utility tests

## Development Workflow

### Current Phase: Backend Foundation ✅
All backend authentication and profile management features are complete and tested.

### Next Phase: Booking Features
1. Create booking schemas and models
2. Implement booking service and repository
3. Add API endpoints for bookings
4. Integrate payment gateway (Razorpay)
5. Build admin functionality
6. Write tests for new features

### Future Phase: Frontend
1. Set up Vite + React + TypeScript project
2. Implement authentication pages
3. Build booking interface
4. Create admin dashboard
5. Integrate with backend API
6. End-to-end testing

## Testing & Quality Assurance

- ✅ All functions have unit tests
- ✅ All API endpoints have integration tests
- ✅ Input validation tested
- ✅ Error scenarios covered
- ✅ Authentication flow tested
- ✅ Test isolation with in-memory database

## Using Postman Collection

1. Import `backend/Resorto.postman_collection.json` into Postman
2. The collection includes:
   - All current API endpoints
   - Auto-save JWT tokens after login/register
   - Pre-configured requests
   - Environment variables

## Environment Variables

Required environment variables (see `backend/.env.example`):

```env
MONGODB_URI=mongodb://localhost:27017
DB_NAME=resorto
JWT_SECRET=your-secret-key-change-this
JWT_EXPIRATION_DAYS=7
```

## Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Protected routes with middleware
- ✅ Email validation
- ✅ Strong password requirements (8+ chars, uppercase, lowercase, number, special char)
- ✅ Input validation with Pydantic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and write tests
4. Ensure all tests pass: `pytest tests/ -v`
5. Submit a pull request

## License

MIT License

## Contact & Support

For questions or issues, please create an issue in the repository.

---

## Next Steps

**Ready to continue development:**
1. ✅ Backend authentication is production-ready
2. 📋 Review and test the backend API
3. 🚀 Start implementing booking system features
4. 🎨 Begin frontend development
5. 🔗 Integrate frontend with backend
6. 🚢 Deploy to production

**To test the current implementation:**
```bash
cd backend
./test.sh        # Run all tests
./run.sh         # Start the server
# Visit http://localhost:8000/docs to try the API
```
