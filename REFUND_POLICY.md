# Resorto - Refund Policy & Implementation

## Overview

Resorto implements an **automatic refund system** that processes refunds based on cancellation timing. The system is designed to be fair to both customers and the business.

## Refund Policy

### User Cancellations

**Automatic Refund Rules:**

| Cancellation Timing | Refund Amount | Refund Percentage |
|---------------------|---------------|-------------------|
| **7+ days before check-in** | Full amount | 100% |
| **Less than 7 days before check-in** | No refund | 0% |

### Admin Cancellations

Admins have **flexible refund options** when cancelling bookings:

**Cancellation with Refund Control:**
- Use: `POST /admin/bookings/{booking_id}/cancel`
- Can choose from 4 refund options:

| Option | Description | Use Case |
|--------|-------------|----------|
| **auto** | Apply 7-day rule (default) | Standard cancellations |
| **full** | 100% refund regardless of timing | Customer service, complaints |
| **partial** | Specify custom amount | Negotiate with customer |
| **none** | No refund regardless of timing | Policy violations, no-shows |

**Separate Manual Refund (After Cancellation):**
- Use: `POST /admin/bookings/{booking_id}/refund`
- For refunding already-cancelled bookings
- Can specify custom refund amount

## API Endpoints

### 1. User Cancellation with Auto-Refund

**Endpoint:** `POST /bookings/{booking_id}/cancel`  
**Auth:** User token required  
**Authorization:** User can only cancel their own bookings

**Request:**
```bash
POST /bookings/abc123/cancel
Authorization: Bearer <user_token>
```

**Response (7+ days before check-in):**
```json
{
  "success": true,
  "data": {
    "booking": {
      "id": "abc123",
      "status": "cancelled",
      "paymentStatus": "refunded",
      ...
    },
    "refund": {
      "refundAmount": 2000.0,
      "refundPercentage": 100,
      "daysUntilCheckIn": 10,
      "refundProcessed": true,
      "refundId": "rfnd_xyz"
    }
  },
  "message": "Booking cancelled successfully"
}
```

**Response (Less than 7 days before check-in):**
```json
{
  "success": true,
  "data": {
    "booking": {
      "id": "abc123",
      "status": "cancelled",
      "paymentStatus": "paid",  // Remains paid, no refund
      ...
    },
    "refund": {
      "refundAmount": 0,
      "refundPercentage": 0,
      "daysUntilCheckIn": 3,
      "refundProcessed": false
    }
  },
  "message": "Booking cancelled successfully"
}
```

### 2. Admin Cancellation with Flexible Refund Options

**Endpoint:** `POST /admin/bookings/{booking_id}/cancel`  
**Auth:** Admin token required  
**Authorization:** Admin only

**Request (Auto - 7-day rule):**
```bash
POST /admin/bookings/abc123/cancel
Authorization: Bearer <admin_token>

{
  "reason": "Customer requested cancellation",
  "refundOption": "auto"  // Optional, defaults to "auto"
}
```

**Request (Full Refund - Override):**
```bash
POST /admin/bookings/abc123/cancel
Authorization: Bearer <admin_token>

{
  "reason": "Service issue - full refund as apology",
  "refundOption": "full"
}
```

**Request (Partial Refund):**
```bash
POST /admin/bookings/abc123/cancel
Authorization: Bearer <admin_token>

{
  "reason": "Partial service provided",
  "refundOption": "partial",
  "refundAmount": 1000.0
}
```

**Request (No Refund):**
```bash
POST /admin/bookings/abc123/cancel
Authorization: Bearer <admin_token>

{
  "reason": "Customer no-show",
  "refundOption": "none"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "booking": {
      "id": "abc123",
      "status": "cancelled",
      "paymentStatus": "refunded",
      ...
    },
    "refund": {
      "refundAmount": 1000.0,
      "refundPercentage": 50,
      "daysUntilCheckIn": 3,
      "refundProcessed": true,
      "refundOption": "partial",
      "refundId": "rfnd_xyz"
    },
    "reason": "Partial service provided"
  },
  "message": "Booking cancelled successfully"
}
```

### 3. Admin Manual Refund (Separate from Cancellation)

**Endpoint:** `POST /admin/bookings/{booking_id}/refund`  
**Auth:** Admin token required  
**Authorization:** Admin only  
**Note:** This is for refunding **already-cancelled** bookings or special cases

**Request (Full Refund):**
```bash
POST /admin/bookings/abc123/refund
Authorization: Bearer <admin_token>

{
  "reason": "Customer complaint - poor service",
  "refundAmount": null  // null = full refund
}
```

**Request (Partial Refund):**
```bash
POST /admin/bookings/abc123/refund
Authorization: Bearer <admin_token>

{
  "reason": "Partial refund due to issues",
  "refundAmount": 1000.0  // Partial amount
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "refunded": true,
    "bookingId": "abc123",
    "refundId": "rfnd_xyz",
    "amount": 2000.0,
    "status": "refunded"
  },
  "message": "Refund processed successfully"
}
```

## Implementation Details

### Flow Diagram

```
User/Admin calls Cancel Booking
         ↓
Check booking exists and authorization
         ↓
Check if booking is already cancelled
         ↓
Is payment made? → NO → Cancel booking (no refund)
         ↓ YES
Calculate days until check-in
         ↓
Is days >= 7? → YES → Calculate 100% refund
         ↓ NO
Calculate 0% refund (no refund)
         ↓
If refund amount > 0:
    Call Razorpay API to process refund
    Update booking: paymentStatus = 'refunded'
         ↓
Update booking: status = 'cancelled'
         ↓
Return booking + refund info
```

### Code Implementation

**File:** `backend/modules/booking/booking_service.py`

Key logic:
```python
# Calculate days until check-in
check_in_date = booking.get('checkInDate')
days_until_checkin = (check_in_date - datetime.utcnow()).days

# Apply refund policy
if days_until_checkin >= 7:
    refund_amount = total_amount  # 100%
    refund_percentage = 100
else:
    refund_amount = 0  # 0%
    refund_percentage = 0

# Process refund if eligible
if refund_amount > 0:
    payment_service.refundPayment(booking_id, refund_amount)
```

### Razorpay Integration

**File:** `backend/modules/booking/payment_service.py`

The refund is processed through Razorpay:

```python
def refundPayment(booking_id: str, refund_amount: Optional[float] = None):
    # Get booking and payment details
    booking = booking_repo.getBookingById(booking_id)
    payment_id = booking.get('paymentId')
    
    # Calculate refund amount
    amount_to_refund = refund_amount or booking.get('totalAmount')
    amount_in_paise = int(amount_to_refund * 100)
    
    # Create refund via Razorpay
    refund = razorpay_client.payment.refund(payment_id, amount_in_paise)
    
    # Update booking status
    booking_repo.updatePaymentStatus(booking_id, 'refunded')
    booking_repo.updateBookingStatus(booking_id, 'cancelled')
    
    return refund details
```

## Business Rules

### When Refund is Processed

✅ **Refund IS processed when:**
- User/Admin cancels 7+ days before check-in
- Payment was successfully made (status = 'paid')
- Payment ID exists in booking
- Razorpay refund API call succeeds

❌ **Refund is NOT processed when:**
- Cancelled less than 7 days before check-in
- Booking was never paid (status = 'pending')
- Booking already cancelled
- Razorpay API failure (booking still cancelled, refund marked as failed)

### Edge Cases Handled

1. **Refund API Failure:**
   - Booking is still cancelled
   - Refund info includes error message
   - Admin can retry manually using refund endpoint

2. **Already Cancelled:**
   - Returns 400 Bad Request
   - No duplicate refunds

3. **No Payment Made:**
   - Booking is cancelled
   - No refund attempted
   - refund info is null

4. **Check-in Date Passed:**
   - Days until check-in will be negative
   - No refund (0%)
   - Booking is cancelled

## Database Changes

### Booking Status Flow

```
pending → confirmed → completed
   ↓         ↓
cancelled ← cancelled
```

### Payment Status Flow

```
pending → paid → refunded
   ↓       ↓
failed   cancelled (if unpaid)
```

## Frontend Integration

### Display Refund Policy to User

Before cancellation, show:

```typescript
const daysUntilCheckIn = calculateDays(booking.checkInDate, new Date());

if (daysUntilCheckIn >= 7) {
  showMessage("You will receive a 100% refund");
} else {
  showMessage("No refund will be issued (less than 7 days)");
}
```

### Handle Cancellation Response

```typescript
const response = await api.post(`/bookings/${bookingId}/cancel`);

if (response.data.success) {
  const { booking, refund } = response.data.data;
  
  if (refund && refund.refundProcessed) {
    showSuccess(`Booking cancelled. ₹${refund.refundAmount} refunded.`);
  } else if (refund && refund.refundAmount === 0) {
    showWarning(`Booking cancelled. No refund (${refund.daysUntilCheckIn} days notice).`);
  } else {
    showSuccess(`Booking cancelled.`);
  }
}
```

## Testing Scenarios

### Scenario 1: Early Cancellation (Full Refund)
```
Check-in: 2025-12-10
Cancellation: 2025-12-01
Days until check-in: 9
Expected: 100% refund
```

### Scenario 2: Late Cancellation (No Refund)
```
Check-in: 2025-12-10
Cancellation: 2025-12-06
Days until check-in: 4
Expected: 0% refund
```

### Scenario 3: Boundary Test (Exactly 7 Days)
```
Check-in: 2025-12-10
Cancellation: 2025-12-03
Days until check-in: 7
Expected: 100% refund
```

### Scenario 4: Unpaid Booking Cancellation
```
Booking status: pending
Payment status: pending
Expected: Cancel without refund attempt
```

### Scenario 5: Admin Manual Refund
```
Booking: Paid, check-in in 2 days
Admin action: Manual refund ₹500 (partial)
Expected: ₹500 refunded regardless of policy
```

## Configuration

No additional configuration needed. Refund policy is hardcoded:

```python
REFUND_CUTOFF_DAYS = 7  # Days before check-in for full refund
FULL_REFUND_PERCENTAGE = 100
NO_REFUND_PERCENTAGE = 0
```

To modify policy, update `booking_service.py`:

```python
if days_until_checkin >= 7:  # Change this number
    refund_amount = total_amount
    refund_percentage = 100
```

## Logging

All refund operations are logged:

```
INFO: Refund processed for booking abc123: 2000.0
ERROR: Error processing refund: Payment not found
```

Check logs in `modules/common/logs.txt`

## Security Considerations

✅ **Security Measures:**
- User can only cancel their own bookings
- Admin token required for manual refunds
- Razorpay signature verification prevents fraud
- Payment IDs validated before refund
- Duplicate refund prevention (check status)

## Summary

| Feature | Status |
|---------|--------|
| **Automatic refund on cancellation** | ✅ Implemented |
| **7-day refund policy** | ✅ Implemented |
| **User cancellation** | ✅ Works |
| **Admin cancellation** | ✅ Works |
| **Admin manual refund** | ✅ Works |
| **Razorpay integration** | ✅ Implemented |
| **Error handling** | ✅ Robust |
| **Logging** | ✅ Complete |

---

**The refund system is production-ready and fully automated!** 🎉
