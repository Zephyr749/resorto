from fastapi import APIRouter, Depends, Response, status
from modules.booking import payment_service
from modules.db.booking_schemas import PaymentVerify, AdminRefund
from modules.common.auth_middleware import get_current_user_id
from modules.common.admin_middleware import require_admin
from modules.common.utils import build_response
from modules.common.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=['Payments'])

@router.post('/bookings/{booking_id}/pay')
def create_payment_order(
    booking_id: str,
    response: Response,
    user_id: str = Depends(get_current_user_id)
) -> dict:
    """
    Create a Razorpay order for a booking (User must own the booking).
    Returns order details needed for frontend payment integration.
    """
    try:
        result = payment_service.createPaymentOrder(booking_id, user_id)
        return build_response(True, result.dict(), 'Payment order created successfully')
    except Exception as e:
        logger.error(f'Error creating payment order: {e}')
        # Set appropriate status code
        error_msg = str(e).lower()
        if 'not found' in error_msg:
            response.status_code = status.HTTP_404_NOT_FOUND
        elif 'permission' in error_msg:
            response.status_code = status.HTTP_403_FORBIDDEN
        elif 'cancelled' in error_msg or 'already paid' in error_msg:
            response.status_code = status.HTTP_400_BAD_REQUEST
        elif 'not configured' in error_msg:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to create payment order')

@router.post('/bookings/{booking_id}/verify-payment')
def verify_payment(
    booking_id: str,
    payment_data: PaymentVerify,
    response: Response,
    user_id: str = Depends(get_current_user_id)
) -> dict:
    """
    Verify Razorpay payment signature after payment completion.
    This confirms the payment and updates booking status to 'confirmed'.
    """
    try:
        result = payment_service.verifyPayment(payment_data, booking_id, user_id)
        return build_response(True, result, 'Payment verified successfully')
    except Exception as e:
        logger.error(f'Error verifying payment: {e}')
        # Set appropriate status code
        error_msg = str(e).lower()
        if 'not found' in error_msg:
            response.status_code = status.HTTP_404_NOT_FOUND
        elif 'permission' in error_msg:
            response.status_code = status.HTTP_403_FORBIDDEN
        elif 'verification failed' in error_msg:
            response.status_code = status.HTTP_400_BAD_REQUEST
        elif 'not configured' in error_msg:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to verify payment')

@router.post('/admin/bookings/{booking_id}/refund')
def refund_payment(
    booking_id: str,
    refund_data: AdminRefund,
    response: Response,
    admin_id: str = Depends(require_admin)
) -> dict:
    """
    Process a refund for a booking (Admin only).
    If refundAmount is not provided, full refund is issued.
    """
    try:
        result = payment_service.refundPayment(booking_id, refund_data.refundAmount)
        return build_response(True, result, 'Refund processed successfully')
    except Exception as e:
        logger.error(f'Error processing refund: {e}')
        # Set appropriate status code
        error_msg = str(e).lower()
        if 'not found' in error_msg:
            response.status_code = status.HTTP_404_NOT_FOUND
        elif 'no payment' in error_msg or 'payment id not found' in error_msg:
            response.status_code = status.HTTP_400_BAD_REQUEST
        elif 'not configured' in error_msg:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to process refund')
