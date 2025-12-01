import razorpay
import hmac
import hashlib
from fastapi import HTTPException, status
from modules.common.config import Config
from modules.booking.booking_repo import BookingRepository
from modules.db.booking_schemas import PaymentCreate, PaymentVerify, PaymentResponse
from modules.common.logger import get_logger
from typing import Optional

logger = get_logger(__name__)
booking_repo = BookingRepository()

# Initialize Razorpay client
try:
    razorpay_client = razorpay.Client(
        auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET)
    )
except Exception as e:
    logger.warning(f'Razorpay client initialization failed: {e}')
    razorpay_client = None

def createPaymentOrder(booking_id: str, user_id: str) -> PaymentResponse:
    """
    Create a Razorpay order for a booking.
    The order ID will be used by frontend to initiate payment.
    """
    if not razorpay_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Payment service is not configured'
        )
    
    # Get booking details
    booking = booking_repo.getBookingById(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Booking not found'
        )
    
    # Verify user owns this booking
    if booking.get('userId') != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to pay for this booking'
        )
    
    # Check if booking is in valid state for payment
    if booking.get('status') == 'cancelled':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot pay for cancelled booking'
        )
    
    if booking.get('paymentStatus') == 'paid':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Booking is already paid'
        )
    
    # Create Razorpay order
    try:
        amount_in_paise = int(booking.get('totalAmount', 0) * 100)  # Convert to paise
        
        order_data = {
            'amount': amount_in_paise,
            'currency': 'INR',
            'receipt': f'booking_{booking_id}',
            'notes': {
                'booking_id': booking_id,
                'user_id': user_id
            }
        }
        
        razorpay_order = razorpay_client.order.create(data=order_data)
        
        return PaymentResponse(
            orderId=razorpay_order['id'],
            amount=booking.get('totalAmount', 0),
            currency='INR',
            razorpayKeyId=Config.RAZORPAY_KEY_ID
        )
    
    except Exception as e:
        logger.error(f'Error creating Razorpay order: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to create payment order'
        )

def verifyPayment(payment_data: PaymentVerify, booking_id: str, user_id: str) -> dict:
    """
    Verify Razorpay payment signature and update booking status.
    This should be called after user completes payment on frontend.
    """
    if not razorpay_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Payment service is not configured'
        )
    
    # Get booking details
    booking = booking_repo.getBookingById(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Booking not found'
        )
    
    # Verify user owns this booking
    if booking.get('userId') != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to verify this payment'
        )
    
    # Verify payment signature
    try:
        # Create signature string
        signature_string = f"{payment_data.razorpayOrderId}|{payment_data.razorpayPaymentId}"
        
        # Generate expected signature
        generated_signature = hmac.new(
            Config.RAZORPAY_KEY_SECRET.encode('utf-8'),
            signature_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Verify signature matches
        if generated_signature != payment_data.razorpaySignature:
            logger.error(f'Payment signature verification failed for booking {booking_id}')
            
            # Update payment status to failed
            booking_repo.updatePaymentStatus(booking_id, 'failed')
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Payment verification failed'
            )
        
        # Signature verified - update booking
        booking_repo.updatePaymentStatus(booking_id, 'paid', payment_data.razorpayPaymentId)
        booking_repo.updateBookingStatus(booking_id, 'confirmed')
        
        logger.info(f'Payment verified successfully for booking {booking_id}')
        
        return {
            'verified': True,
            'bookingId': booking_id,
            'paymentId': payment_data.razorpayPaymentId,
            'status': 'confirmed'
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error verifying payment: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to verify payment'
        )

def refundPayment(booking_id: str, refund_amount: Optional[float] = None) -> dict:
    """
    Process a refund for a booking (Admin only).
    If refund_amount is None, full refund is issued.
    """
    if not razorpay_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Payment service is not configured'
        )
    
    # Get booking details
    booking = booking_repo.getBookingById(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Booking not found'
        )
    
    # Check if payment was made
    if booking.get('paymentStatus') != 'paid':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No payment to refund'
        )
    
    payment_id = booking.get('paymentId')
    if not payment_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Payment ID not found'
        )
    
    try:
        # Calculate refund amount
        total_amount = booking.get('totalAmount', 0)
        amount_to_refund = refund_amount if refund_amount else total_amount
        amount_in_paise = int(amount_to_refund * 100)
        
        # Create refund
        refund = razorpay_client.payment.refund(payment_id, amount_in_paise)
        
        # Update booking status
        booking_repo.updatePaymentStatus(booking_id, 'refunded')
        booking_repo.updateBookingStatus(booking_id, 'cancelled')
        
        logger.info(f'Refund processed for booking {booking_id}: {amount_to_refund}')
        
        return {
            'refunded': True,
            'bookingId': booking_id,
            'refundId': refund['id'],
            'amount': amount_to_refund,
            'status': 'refunded'
        }
    
    except Exception as e:
        logger.error(f'Error processing refund: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to process refund'
        )
