from fastapi import HTTPException, status
from modules.booking.booking_repo import BookingRepository
from modules.auth.auth_repo import AuthRepository
from modules.db.booking_schemas import (
    SpotCreate, SpotUpdate, Spot, 
    BookingCreate, BookingUpdate, Booking, BookingWithDetails,
    BookingStatus, PaymentStatus, AvailabilityResponse, BookingStats
)
from modules.common.logger import get_logger
from datetime import datetime
from typing import List, Optional

logger = get_logger(__name__)
booking_repo = BookingRepository()
auth_repo = AuthRepository()

# Spot Service Functions
def createSpot(spot: SpotCreate) -> Spot:
    """Create a new spot/room (Admin only)"""
    try:
        spot_id = booking_repo.createSpot(spot)
        created_spot = booking_repo.getSpotById(spot_id)
        return _buildSpotObject(created_spot, spot_id)
    except Exception as e:
        logger.error(f'Error creating spot: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to create spot'
        )

def getSpot(spot_id: str) -> Spot:
    """Get a single spot by ID"""
    spot = booking_repo.getSpotById(spot_id)
    if not spot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Spot not found'
        )
    return _buildSpotObject(spot, spot_id)

def getAllSpots(is_active: Optional[bool] = True, spot_type: Optional[str] = None) -> List[Spot]:
    """Get all spots with optional filtering"""
    spots = booking_repo.getAllSpots(is_active, spot_type)
    return [_buildSpotObject(spot, str(spot['_id'])) for spot in spots]

def updateSpot(spot_id: str, spot_update: SpotUpdate) -> Spot:
    """Update a spot (Admin only)"""
    spot = booking_repo.getSpotById(spot_id)
    if not spot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Spot not found'
        )
    
    success = booking_repo.updateSpot(spot_id, spot_update)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to update spot'
        )
    
    updated_spot = booking_repo.getSpotById(spot_id)
    return _buildSpotObject(updated_spot, spot_id)

def deleteSpot(spot_id: str) -> dict:
    """Soft delete a spot (Admin only)"""
    spot = booking_repo.getSpotById(spot_id)
    if not spot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Spot not found'
        )
    
    success = booking_repo.deleteSpot(spot_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete spot'
        )
    
    return {'message': 'Spot deleted successfully'}

# Booking Service Functions
def checkAvailability(spot_id: str, check_in: datetime, check_out: datetime) -> AvailabilityResponse:
    """Check if a spot is available for the given dates"""
    # Validate dates
    if check_in >= check_out:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Check-out date must be after check-in date'
        )
    
    if check_in < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Check-in date cannot be in the past'
        )
    
    # Check if spot exists
    spot = booking_repo.getSpotById(spot_id)
    if not spot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Spot not found'
        )
    
    # Check for conflicts
    conflicts = booking_repo.getConflictingBookings(spot_id, check_in, check_out)
    
    return AvailabilityResponse(
        spotId=spot_id,
        isAvailable=len(conflicts) == 0,
        conflictingBookings=[str(b['_id']) for b in conflicts]
    )

def createBooking(booking: BookingCreate, user_id: str) -> Booking:
    """Create a new booking"""
    # Validate dates
    if booking.checkInDate >= booking.checkOutDate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Check-out date must be after check-in date'
        )
    
    if booking.checkInDate < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Check-in date cannot be in the past'
        )
    
    # Check if spot exists and is active
    spot = booking_repo.getSpotById(booking.spotId)
    if not spot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Spot not found'
        )
    
    if not spot.get('isActive', True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Spot is not available for booking'
        )
    
    # Check availability
    conflicts = booking_repo.getConflictingBookings(booking.spotId, booking.checkInDate, booking.checkOutDate)
    if conflicts:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Spot is not available for the selected dates'
        )
    
    # Validate capacity
    if booking.numberOfGuests > spot.get('capacity', 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Number of guests exceeds spot capacity ({spot.get("capacity")})'
        )
    
    # Calculate total amount
    days = (booking.checkOutDate - booking.checkInDate).days
    total_amount = days * spot.get('pricePerDay', 0)
    
    # Create booking
    booking_id = booking_repo.createBooking(booking, user_id, total_amount)
    created_booking = booking_repo.getBookingById(booking_id)
    
    return _buildBookingObject(created_booking, booking_id)

def getBooking(booking_id: str, user_id: str, is_admin: bool = False) -> BookingWithDetails:
    """Get a booking by ID with full details"""
    booking = booking_repo.getBookingById(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Booking not found'
        )
    
    # Check authorization (user can only see their own bookings, admin can see all)
    if not is_admin and booking.get('userId') != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to view this booking'
        )
    
    return _buildBookingWithDetails(booking, str(booking['_id']))

def getUserBookings(user_id: str) -> List[BookingWithDetails]:
    """Get all bookings for a user"""
    bookings = booking_repo.getUserBookings(user_id)
    return [_buildBookingWithDetails(b, str(b['_id'])) for b in bookings]

def getAllBookings(status: Optional[str] = None) -> List[BookingWithDetails]:
    """Get all bookings (Admin only)"""
    bookings = booking_repo.getAllBookings(status)
    return [_buildBookingWithDetails(b, str(b['_id'])) for b in bookings]

def cancelBooking(booking_id: str, user_id: str, is_admin: bool = False, admin_refund_option: str = "auto", admin_refund_amount: Optional[float] = None) -> dict:
    """
    Cancel a booking with refund processing.
    
    User Refund Policy:
    - Cancelled 7+ days before check-in: 100% refund
    - Cancelled less than 7 days before check-in: No refund
    
    Admin Refund Options (admin_refund_option):
    - "auto": Apply automatic 7-day rule (default)
    - "full": Full refund regardless of timing
    - "partial": Partial refund (requires admin_refund_amount)
    - "none": No refund regardless of timing
    """
    booking = booking_repo.getBookingById(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Booking not found'
        )
    
    # Check authorization
    if not is_admin and booking.get('userId') != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to cancel this booking'
        )
    
    # Check if already cancelled
    if booking.get('status') == 'cancelled':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Booking is already cancelled'
        )
    
    # Check if payment was made
    payment_status = booking.get('paymentStatus', 'pending')
    payment_id = booking.get('paymentId')
    should_refund = payment_status == 'paid' and payment_id
    
    refund_info = None
    
    if should_refund:
        # Calculate refund amount based on cancellation timing or admin override
        check_in_date = booking.get('checkInDate')
        total_amount = booking.get('totalAmount', 0)
        days_until_checkin = (check_in_date - datetime.utcnow()).days
        
        # Admin can override refund logic
        if is_admin and admin_refund_option != "auto":
            if admin_refund_option == "full":
                refund_amount = total_amount
                refund_percentage = 100
            elif admin_refund_option == "partial":
                if admin_refund_amount is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Partial refund amount is required'
                    )
                if admin_refund_amount > total_amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Refund amount cannot exceed total amount'
                    )
                refund_amount = admin_refund_amount
                refund_percentage = int((refund_amount / total_amount) * 100)
            elif admin_refund_option == "none":
                refund_amount = 0
                refund_percentage = 0
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid refund option. Use: auto, full, partial, or none'
                )
        else:
            # Standard 7-day policy for users and admin "auto" option
            if days_until_checkin >= 7:
                # Full refund (100%)
                refund_amount = total_amount
                refund_percentage = 100
            else:
                # No refund
                refund_amount = 0
                refund_percentage = 0
        
        refund_info = {
            'refundAmount': refund_amount,
            'refundPercentage': refund_percentage,
            'daysUntilCheckIn': days_until_checkin,
            'refundProcessed': False,
            'refundOption': admin_refund_option if is_admin else 'auto'
        }
        
        # Process refund if amount > 0
        if refund_amount > 0:
            try:
                # Import here to avoid circular dependency
                from modules.booking import payment_service
                
                refund_result = payment_service.refundPayment(booking_id, refund_amount)
                refund_info['refundProcessed'] = True
                refund_info['refundId'] = refund_result.get('refundId')
                
                logger.info(f'Refund processed for booking {booking_id}: {refund_amount}')
            except Exception as e:
                logger.error(f'Error processing refund: {e}')
                # Continue with cancellation even if refund fails
                refund_info['refundError'] = str(e)
    
    # Update booking status
    success = booking_repo.updateBookingStatus(booking_id, 'cancelled')
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to cancel booking'
        )
    
    updated_booking = booking_repo.getBookingById(booking_id)
    booking_obj = _buildBookingObject(updated_booking, booking_id)
    
    # Return booking with refund information
    return {
        'booking': booking_obj,
        'refund': refund_info
    }

def updateBookingPayment(booking_id: str, payment_status: str, payment_id: Optional[str] = None) -> Booking:
    """Update booking payment status"""
    booking = booking_repo.getBookingById(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Booking not found'
        )
    
    success = booking_repo.updatePaymentStatus(booking_id, payment_status, payment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to update payment status'
        )
    
    # If payment is successful, confirm the booking
    if payment_status == 'paid':
        booking_repo.updateBookingStatus(booking_id, 'confirmed')
    
    updated_booking = booking_repo.getBookingById(booking_id)
    return _buildBookingObject(updated_booking, booking_id)

def getBookingStats() -> BookingStats:
    """Get booking statistics (Admin only)"""
    stats = booking_repo.getBookingStats()
    return BookingStats(**stats)

# Helper Functions
def _buildSpotObject(spot_dict: dict, spot_id: str) -> Spot:
    """Build Spot object from database dict"""
    return Spot(
        id=spot_id,
        name=spot_dict['name'],
        description=spot_dict['description'],
        spotType=spot_dict['spotType'],
        capacity=spot_dict['capacity'],
        pricePerDay=spot_dict['pricePerDay'],
        amenities=spot_dict.get('amenities', []),
        images=spot_dict.get('images', []),
        isActive=spot_dict.get('isActive', True),
        createdAt=spot_dict['createdAt'],
        updatedAt=spot_dict['updatedAt']
    )

def _buildBookingObject(booking_dict: dict, booking_id: str) -> Booking:
    """Build Booking object from database dict"""
    return Booking(
        id=booking_id,
        userId=booking_dict['userId'],
        spotId=booking_dict['spotId'],
        checkInDate=booking_dict['checkInDate'],
        checkOutDate=booking_dict['checkOutDate'],
        numberOfGuests=booking_dict['numberOfGuests'],
        specialRequests=booking_dict.get('specialRequests'),
        status=booking_dict.get('status', 'pending'),
        totalAmount=booking_dict['totalAmount'],
        paymentStatus=booking_dict.get('paymentStatus', 'pending'),
        paymentId=booking_dict.get('paymentId'),
        createdAt=booking_dict['createdAt'],
        updatedAt=booking_dict['updatedAt']
    )

def _buildBookingWithDetails(booking_dict: dict, booking_id: str) -> BookingWithDetails:
    """Build BookingWithDetails object with spot and user info"""
    # Get spot details
    spot = booking_repo.getSpotById(booking_dict['spotId'])
    spot_obj = _buildSpotObject(spot, booking_dict['spotId']) if spot else None
    
    # Get user details
    user = auth_repo.getUserById(booking_dict['userId'])
    user_name = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip() if user else "Unknown"
    user_email = user.get('email', '') if user else ''
    
    return BookingWithDetails(
        id=booking_id,
        userId=booking_dict['userId'],
        spotId=booking_dict['spotId'],
        checkInDate=booking_dict['checkInDate'],
        checkOutDate=booking_dict['checkOutDate'],
        numberOfGuests=booking_dict['numberOfGuests'],
        specialRequests=booking_dict.get('specialRequests'),
        status=booking_dict.get('status', 'pending'),
        totalAmount=booking_dict['totalAmount'],
        paymentStatus=booking_dict.get('paymentStatus', 'pending'),
        paymentId=booking_dict.get('paymentId'),
        createdAt=booking_dict['createdAt'],
        updatedAt=booking_dict['updatedAt'],
        spot=spot_obj,
        userName=user_name,
        userEmail=user_email
    )
