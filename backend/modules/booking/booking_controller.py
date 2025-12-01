from fastapi import APIRouter, Depends, Response, status
from modules.booking import booking_service
from modules.db.booking_schemas import (
    Spot, BookingCreate, Booking, BookingWithDetails,
    AvailabilityCheck, AvailabilityResponse
)
from modules.common.auth_middleware import get_current_user_id
from modules.common.utils import build_response
from modules.common.logger import get_logger
from typing import List, Optional

logger = get_logger(__name__)
router = APIRouter()

# Public Endpoints (No Auth Required)

@router.get('/spots', tags=['Spots'])
def get_spots(spot_type: Optional[str] = None) -> dict:
    """
    Get all active spots/rooms.
    Query params:
    - spot_type: Filter by 'picnic_area' or 'room' (optional)
    """
    try:
        spots = booking_service.getAllSpots(is_active=True, spot_type=spot_type)
        return build_response(True, {'spots': [spot.dict() for spot in spots]}, 'Spots retrieved successfully')
    except Exception as e:
        logger.error(f'Error getting spots: {e}')
        return build_response(False, str(e), 'Failed to get spots')

@router.get('/spots/{spot_id}', tags=['Spots'])
def get_spot(spot_id: str, response: Response) -> dict:
    """Get details of a specific spot/room"""
    try:
        spot = booking_service.getSpot(spot_id)
        return build_response(True, {'spot': spot.dict()}, 'Spot retrieved successfully')
    except Exception as e:
        logger.error(f'Error getting spot: {e}')
        # Set appropriate status code
        if 'not found' in str(e).lower():
            response.status_code = status.HTTP_404_NOT_FOUND
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to get spot')

@router.post('/bookings/check-availability', tags=['Bookings'])
def check_availability(check: AvailabilityCheck, response: Response) -> dict:
    """
    Check if a spot is available for given dates.
    Returns availability status and conflicting booking IDs if any.
    """
    try:
        result = booking_service.checkAvailability(
            check.spotId, 
            check.checkInDate, 
            check.checkOutDate
        )
        return build_response(True, result.dict(), 'Availability checked successfully')
    except Exception as e:
        logger.error(f'Error checking availability: {e}')
        # Set appropriate status code
        if 'not found' in str(e).lower():
            response.status_code = status.HTTP_404_NOT_FOUND
        elif 'past' in str(e).lower() or 'after' in str(e).lower():
            response.status_code = status.HTTP_400_BAD_REQUEST
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to check availability')

# User Endpoints (Auth Required)

@router.post('/bookings', tags=['Bookings'])
def create_booking(
    booking: BookingCreate, 
    response: Response,
    user_id: str = Depends(get_current_user_id)
) -> dict:
    """
    Create a new booking (requires authentication).
    The booking will be in 'pending' status until payment is completed.
    """
    try:
        result = booking_service.createBooking(booking, user_id)
        return build_response(True, {'booking': result.dict()}, 'Booking created successfully')
    except Exception as e:
        logger.error(f'Error creating booking: {e}')
        # Set appropriate status code
        error_msg = str(e).lower()
        if 'not found' in error_msg:
            response.status_code = status.HTTP_404_NOT_FOUND
        elif 'not available' in error_msg or 'past' in error_msg or 'after' in error_msg or 'exceeds' in error_msg:
            response.status_code = status.HTTP_400_BAD_REQUEST
        elif 'conflict' in error_msg:
            response.status_code = status.HTTP_409_CONFLICT
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to create booking')

@router.get('/bookings/my-bookings', tags=['Bookings'])
def get_my_bookings(user_id: str = Depends(get_current_user_id)) -> dict:
    """Get all bookings for the authenticated user"""
    try:
        bookings = booking_service.getUserBookings(user_id)
        return build_response(
            True, 
            {'bookings': [booking.dict() for booking in bookings]}, 
            'Bookings retrieved successfully'
        )
    except Exception as e:
        logger.error(f'Error getting user bookings: {e}')
        return build_response(False, str(e), 'Failed to get bookings')

@router.get('/bookings/{booking_id}', tags=['Bookings'])
def get_booking(
    booking_id: str, 
    response: Response,
    user_id: str = Depends(get_current_user_id)
) -> dict:
    """Get details of a specific booking (user can only see their own bookings)"""
    try:
        booking = booking_service.getBooking(booking_id, user_id, is_admin=False)
        return build_response(True, {'booking': booking.dict()}, 'Booking retrieved successfully')
    except Exception as e:
        logger.error(f'Error getting booking: {e}')
        # Set appropriate status code
        error_msg = str(e).lower()
        if 'not found' in error_msg:
            response.status_code = status.HTTP_404_NOT_FOUND
        elif 'permission' in error_msg:
            response.status_code = status.HTTP_403_FORBIDDEN
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to get booking')

@router.post('/bookings/{booking_id}/cancel', tags=['Bookings'])
def cancel_booking(
    booking_id: str, 
    response: Response,
    user_id: str = Depends(get_current_user_id)
) -> dict:
    """
    Cancel a booking (user can only cancel their own bookings).
    
    Refund Policy:
    - Cancelled 7+ days before check-in: 100% refund
    - Cancelled less than 7 days before check-in: No refund
    """
    try:
        result = booking_service.cancelBooking(booking_id, user_id, is_admin=False)
        
        # Convert booking object to dict
        response_data = {
            'booking': result['booking'].dict(),
            'refund': result['refund']
        }
        
        return build_response(True, response_data, 'Booking cancelled successfully')
    except Exception as e:
        logger.error(f'Error cancelling booking: {e}')
        # Set appropriate status code
        error_msg = str(e).lower()
        if 'not found' in error_msg:
            response.status_code = status.HTTP_404_NOT_FOUND
        elif 'permission' in error_msg:
            response.status_code = status.HTTP_403_FORBIDDEN
        elif 'already' in error_msg:
            response.status_code = status.HTTP_400_BAD_REQUEST
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to cancel booking')
