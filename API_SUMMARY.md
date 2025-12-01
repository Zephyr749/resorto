# Resorto API - Quick Reference

## Base URL
```
http://localhost:8000
```

## API Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 1. Authentication APIs

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "firstName": "John",
  "lastName": "Doe"
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "data": {
    "user": { "id": "...", "email": "...", "role": "user" },
    "token": "eyJ..."
  }
}
```

### Get Profile
```http
GET /auth/profile
Authorization: Bearer <token>
```

### Update Profile
```http
PUT /auth/profile
Authorization: Bearer <token>

{
  "firstName": "Jane",
  "lastName": "Smith"
}
```

### Change Password
```http
POST /auth/change-password
Authorization: Bearer <token>

{
  "currentPassword": "old123",
  "newPassword": "new456"
}
```

---

## 2. Public Spot APIs (No Auth)

### Get All Spots
```http
GET /spots?spotType=picnic_area
```

### Get Spot Details
```http
GET /spots/{spot_id}
```

### Check Availability
```http
POST /bookings/check-availability

{
  "spotId": "spot_id",
  "checkInDate": "2025-12-01T12:00:00Z",
  "checkOutDate": "2025-12-02T12:00:00Z"
}
```

---

## 3. User Booking APIs (Auth Required)

### Create Booking
```http
POST /bookings
Authorization: Bearer <token>

{
  "spotId": "spot_id",
  "checkInDate": "2025-12-01T12:00:00Z",
  "checkOutDate": "2025-12-02T12:00:00Z",
  "numberOfGuests": 5,
  "specialRequests": "Extra chairs needed"
}
```

### Get My Bookings
```http
GET /bookings/my-bookings
Authorization: Bearer <token>
```

### Get Booking Details
```http
GET /bookings/{booking_id}
Authorization: Bearer <token>
```

### Cancel Booking (User)
```http
POST /bookings/{booking_id}/cancel
Authorization: Bearer <token>

Response:
{
  "success": true,
  "data": {
    "booking": { ... },
    "refund": {
      "refundAmount": 2000.0,
      "refundPercentage": 100,
      "daysUntilCheckIn": 10,
      "refundProcessed": true
    }
  }
}
```
**Refund Policy:** 7+ days before = 100%, <7 days = 0%

---

## 4. Payment APIs (Auth Required)

### Initiate Payment
```http
POST /bookings/{booking_id}/pay
Authorization: Bearer <token>

Response:
{
  "success": true,
  "data": {
    "orderId": "order_xyz",
    "amount": 2000.0,
    "currency": "INR",
    "razorpayKeyId": "rzp_test_..."
  }
}
```

### Verify Payment
```http
POST /bookings/{booking_id}/verify-payment
Authorization: Bearer <token>

{
  "razorpayOrderId": "order_xyz",
  "razorpayPaymentId": "pay_abc",
  "razorpaySignature": "signature_hash"
}
```

---

## 5. Admin - Spot Management (Admin Only)

### Create Spot
```http
POST /admin/spots
Authorization: Bearer <admin_token>

{
  "name": "Lakeside Picnic Area",
  "description": "Beautiful spot by the lake",
  "spotType": "picnic_area",
  "capacity": 15,
  "pricePerDay": 2000.0,
  "amenities": ["BBQ", "Tables", "Parking"],
  "images": ["/images/lakeside1.jpg"]
}
```

### Update Spot
```http
PUT /admin/spots/{spot_id}
Authorization: Bearer <admin_token>

{
  "pricePerDay": 2500.0,
  "isActive": true
}
```

### Delete Spot (Soft Delete)
```http
DELETE /admin/spots/{spot_id}
Authorization: Bearer <admin_token>
```

### Get All Spots (Including Inactive)
```http
GET /admin/spots?isActive=false
Authorization: Bearer <admin_token>
```

---

## 6. Admin - Booking Management (Admin Only)

### Get All Bookings
```http
GET /admin/bookings?status=confirmed
Authorization: Bearer <admin_token>
```

### Get Booking Details
```http
GET /admin/bookings/{booking_id}
Authorization: Bearer <admin_token>
```

### Cancel Booking (Admin with Options)
```http
POST /admin/bookings/{booking_id}/cancel
Authorization: Bearer <admin_token>

# Option 1: Auto (7-day rule)
{
  "reason": "Customer requested",
  "refundOption": "auto"
}

# Option 2: Full Refund
{
  "reason": "Service issue - apology",
  "refundOption": "full"
}

# Option 3: Partial Refund
{
  "reason": "Partial service",
  "refundOption": "partial",
  "refundAmount": 1000.0
}

# Option 4: No Refund
{
  "reason": "Customer no-show",
  "refundOption": "none"
}
```

### Process Manual Refund
```http
POST /admin/bookings/{booking_id}/refund
Authorization: Bearer <admin_token>

{
  "reason": "Customer complaint",
  "refundAmount": 1500.0  // null for full refund
}
```

### Get Statistics
```http
GET /admin/bookings/stats/overview
Authorization: Bearer <admin_token>

Response:
{
  "success": true,
  "data": {
    "stats": {
      "totalBookings": 25,
      "confirmedBookings": 18,
      "pendingBookings": 5,
      "cancelledBookings": 2,
      "totalRevenue": 45000.0,
      "todayBookings": 3
    }
  }
}
```

---

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description",
  "message": "Operation failed"
}
```

---

## HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful operation |
| 400 | Bad Request | Invalid input, validation error |
| 401 | Unauthorized | Invalid credentials, missing token |
| 403 | Forbidden | Not admin, not owner |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Booking not available (dates conflict) |
| 500 | Server Error | Database error, server issue |
| 503 | Service Unavailable | Payment gateway not configured |

---

## Quick Start Examples

### 1. User Journey: Book a Spot

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"pass123","firstName":"John","lastName":"Doe"}'

# 2. Login (save token)
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"pass123"}' \
  | jq -r '.data.token')

# 3. Browse spots
curl http://localhost:8000/spots

# 4. Check availability
curl -X POST http://localhost:8000/bookings/check-availability \
  -H "Content-Type: application/json" \
  -d '{"spotId":"spot123","checkInDate":"2025-12-01T12:00:00Z","checkOutDate":"2025-12-02T12:00:00Z"}'

# 5. Create booking
BOOKING_ID=$(curl -X POST http://localhost:8000/bookings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"spotId":"spot123","checkInDate":"2025-12-01T12:00:00Z","checkOutDate":"2025-12-02T12:00:00Z","numberOfGuests":5}' \
  | jq -r '.data.booking.id')

# 6. Pay for booking
curl -X POST http://localhost:8000/bookings/$BOOKING_ID/pay \
  -H "Authorization: Bearer $TOKEN"

# 7. View my bookings
curl http://localhost:8000/bookings/my-bookings \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Admin Journey: Manage Spots & Bookings

```bash
# 1. Login as admin
ADMIN_TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@resorto.com","password":"admin123"}' \
  | jq -r '.data.token')

# 2. Create spot
curl -X POST http://localhost:8000/admin/spots \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Lakeside","description":"Lake view","spotType":"picnic_area","capacity":15,"pricePerDay":2000,"amenities":["BBQ"]}'

# 3. View all bookings
curl http://localhost:8000/admin/bookings \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# 4. View statistics
curl http://localhost:8000/admin/bookings/stats/overview \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# 5. Cancel booking with full refund
curl -X POST http://localhost:8000/admin/bookings/booking123/cancel \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason":"Service issue","refundOption":"full"}'
```

---

## Environment Setup

### Required Environment Variables

```bash
# .env file
MONGODB_URI=mongodb://localhost:27017
DB_NAME=resorto
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# Razorpay (get from dashboard.razorpay.com)
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=your_secret_here
```

### Start Server

```bash
cd backend
./run.sh
# Server starts on http://localhost:8000
```

---

## Testing with Postman

Import the collection:
```
backend/Resorto.postman_collection.json
```

Features:
- All endpoints pre-configured
- Auto-token management
- Example requests

---

## Need Help?

- **API Docs:** http://localhost:8000/docs
- **Development Guide:** `/DEVELOPMENT_GUIDE.md`
- **Refund Policy:** `/REFUND_POLICY.md`
- **Project Status:** `/PROJECT_STATUS.md`

---

**Total Endpoints:** 23  
**Public:** 3 | **User:** 7 | **Admin:** 13
