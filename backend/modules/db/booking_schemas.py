from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums
class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class SpotType(str, Enum):
    PICNIC_AREA = "picnic_area"
    ROOM = "room"

# Spot/Room Models
class SpotBase(BaseModel):
    name: str
    description: str
    spotType: SpotType
    capacity: int
    pricePerDay: float
    amenities: List[str] = []
    images: List[str] = []  # Image paths/URLs
    isActive: bool = True

class SpotCreate(SpotBase):
    pass

class SpotUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    pricePerDay: Optional[float] = None
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None
    isActive: Optional[bool] = None

class Spot(SpotBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

# Booking Models
class BookingBase(BaseModel):
    spotId: str
    checkInDate: datetime
    checkOutDate: datetime
    numberOfGuests: int
    specialRequests: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    checkInDate: Optional[datetime] = None
    checkOutDate: Optional[datetime] = None
    numberOfGuests: Optional[int] = None
    specialRequests: Optional[str] = None
    status: Optional[BookingStatus] = None

class Booking(BookingBase):
    id: str
    userId: str
    status: BookingStatus = BookingStatus.PENDING
    totalAmount: float
    paymentStatus: PaymentStatus = PaymentStatus.PENDING
    paymentId: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class BookingWithDetails(Booking):
    spot: Spot
    userName: str
    userEmail: str

# Payment Models
class PaymentCreate(BaseModel):
    bookingId: str
    amount: float

class PaymentVerify(BaseModel):
    razorpayOrderId: str
    razorpayPaymentId: str
    razorpaySignature: str

class PaymentResponse(BaseModel):
    orderId: str
    amount: float
    currency: str = "INR"
    razorpayKeyId: str

# Admin Models
class BookingStats(BaseModel):
    totalBookings: int
    confirmedBookings: int
    pendingBookings: int
    cancelledBookings: int
    totalRevenue: float
    todayBookings: int

class AdminRefund(BaseModel):
    reason: str
    refundAmount: Optional[float] = None  # If None, full refund

class AdminCancelBooking(BaseModel):
    reason: str
    refundOption: str = "auto"  # "auto", "full", "partial", "none"
    refundAmount: Optional[float] = None  # Required if refundOption is "partial"

# Availability Models
class AvailabilityCheck(BaseModel):
    spotId: str
    checkInDate: datetime
    checkOutDate: datetime

class AvailabilityResponse(BaseModel):
    spotId: str
    isAvailable: bool
    conflictingBookings: List[str] = []  # Booking IDs that conflict
