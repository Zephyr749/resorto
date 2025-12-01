from fastapi import APIRouter, Depends, Response, status
from modules.booking import booking_service
from modules.db.booking_schemas import (
    SpotCreate, SpotUpdate, Spot, BookingWithDetails, BookingStats, AdminCancelBooking
)
from modules.common.admin_middleware import require_admin
from modules.common.utils import build_response
from modules.common.logger import get_logger
from typing import Optional

logger = get_logger(__name__)
router = APIRouter(prefix='/admin', tags=['Admin'])

# Spot Management

@router.post('/spots')
def create_spot(
    spot: SpotCreate, 
    response: Response,
    admin_id: str = Depends(require_admin)
) -> dict:
    """Create a new spot/room (Admin only)"""
    try:
        result = booking_service.createSpot(spot)
        return build_response(True, {'spot': result.dict()}, 'Spot created successfully')
    except Exception as e:
        logger.error(f'Error creating spot: {e}')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to create spot')

@router.put('/spots/{spot_id}')
def update_spot(
    spot_id: str,
    spot_update: SpotUpdate,
    response: Response,
    admin_id: str = Depends(require_admin)
) -> dict:
    """Update an existing spot/room (Admin only)"""
    try:
        result = booking_service.updateSpot(spot_id, spot_update)
        return build_response(True, {'spot': result.dict()}, 'Spot updated successfully')
    except Exception as e:
        logger.error(f'Error updating spot: {e}')
        if 'not found' in str(e).lower():
            response.status_code = status.HTTP_404_NOT_FOUND
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to update spot')

@router.delete('/spots/{spot_id}')
def delete_spot(
    spot_id: str,
    response: Response,
    admin_id: str = Depends(require_admin)
) -> dict:
    """Soft delete a spot/room (Admin only)"""
    try:
        result = booking_service.deleteSpot(spot_id)
        return build_response(True, result, 'Spot deleted successfully')
    except Exception as e:
        logger.error(f'Error deleting spot: {e}')
        if 'not found' in str(e).lower():
            response.status_code = status.HTTP_404_NOT_FOUND
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to delete spot')

@router.get('/spots')
def get_all_spots_admin(
    is_active: Optional[bool] = None,
    spot_type: Optional[str] = None,
    admin_id: str = Depends(require_admin)
) -> dict:
    """Get all spots including inactive ones (Admin only)"""
    try:
        spots = booking_service.getAllSpots(is_active=is_active, spot_type=spot_type)
        return build_response(True, {'spots': [spot.dict() for spot in spots]}, 'Spots retrieved successfully')
    except Exception as e:
        logger.error(f'Error getting spots: {e}')
        return build_response(False, str(e), 'Failed to get spots')

# Booking Management

@router.get('/bookings')
def get_all_bookings(
    booking_status: Optional[str] = None,
    admin_id: str = Depends(require_admin)
) -> dict:
    """
    Get all bookings (Admin only).
    Query params:
    - booking_status: Filter by 'pending', 'confirmed', 'cancelled', or 'completed' (optional)
    """
    try:
        bookings = booking_service.getAllBookings(status=booking_status)
        return build_response(
            True, 
            {'bookings': [booking.dict() for booking in bookings]}, 
            'Bookings retrieved successfully'
        )
    except Exception as e:
        logger.error(f'Error getting all bookings: {e}')
        return build_response(False, str(e), 'Failed to get bookings')

@router.get('/bookings/{booking_id}')
def get_booking_admin(
    booking_id: str,
    response: Response,
    admin_id: str = Depends(require_admin)
) -> dict:
    """Get booking details with full information (Admin only)"""
    try:
        booking = booking_service.getBooking(booking_id, admin_id, is_admin=True)
        return build_response(True, {'booking': booking.dict()}, 'Booking retrieved successfully')
    except Exception as e:
        logger.error(f'Error getting booking: {e}')
        if 'not found' in str(e).lower():
            response.status_code = status.HTTP_404_NOT_FOUND
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to get booking')

@router.post('/bookings/{booking_id}/cancel')
def cancel_booking_admin(
    booking_id: str,
    cancel_data: AdminCancelBooking,
    response: Response,
    admin_id: str = Depends(require_admin)
) -> dict:
    """
    Cancel any booking with flexible refund options (Admin only).
    
    Request Body:
    {
      "reason": "Customer complaint",
      "refundOption": "auto|full|partial|none",  // Default: "auto"
      "refundAmount": 1000.0  // Required only if refundOption is "partial"
    }
    
    Refund Options:
    - "auto": Apply automatic 7-day rule (7+ days = 100%, <7 days = 0%)
    - "full": Full refund regardless of timing
    - "partial": Partial refund (specify refundAmount)
    - "none": No refund regardless of timing
    """
    try:
        result = booking_service.cancelBooking(
            booking_id, 
            admin_id, 
            is_admin=True,
            admin_refund_option=cancel_data.refundOption,
            admin_refund_amount=cancel_data.refundAmount
        )
        
        # Convert booking object to dict
        response_data = {
            'booking': result['booking'].dict(),
            'refund': result['refund'],
            'reason': cancel_data.reason
        }
        
        return build_response(True, response_data, 'Booking cancelled successfully')
    except Exception as e:
        logger.error(f'Error cancelling booking: {e}')
        error_msg = str(e).lower()
        if 'not found' in error_msg:
            response.status_code = status.HTTP_404_NOT_FOUND
        elif 'already' in error_msg or 'invalid refund' in error_msg or 'required' in error_msg or 'exceed' in error_msg:
            response.status_code = status.HTTP_400_BAD_REQUEST
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to cancel booking')

# Statistics

@router.get('/bookings/stats/overview')
def get_booking_stats(admin_id: str = Depends(require_admin)) -> dict:
    """
    Get booking statistics (Admin only).
    Returns total bookings, confirmed, pending, cancelled, revenue, and today's bookings.
    """
    try:
        stats = booking_service.getBookingStats()
        return build_response(True, {'stats': stats.dict()}, 'Statistics retrieved successfully')
    except Exception as e:
        logger.error(f'Error getting booking stats: {e}')
        return build_response(False, str(e), 'Failed to get statistics')
