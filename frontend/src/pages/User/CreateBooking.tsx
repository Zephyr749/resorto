import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { DatePicker, message, Spin, InputNumber } from 'antd';
import { spotsApi } from '../../api/spots';
import { bookingsApi } from '../../api/bookings';
import { Spot } from '../../types';
import dayjs, { Dayjs } from 'dayjs';

const { RangePicker } = DatePicker;

declare global {
  interface Window {
    Razorpay: any;
  }
}

const CreateBooking = () => {
  const { spotId } = useParams<{ spotId: string }>();
  const navigate = useNavigate();
  const [spot, setSpot] = useState<Spot | null>(null);
  const [loading, setLoading] = useState(true);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [dates, setDates] = useState<[Dayjs, Dayjs] | null>(null);
  const [guests, setGuests] = useState(1);
  const [specialRequests, setSpecialRequests] = useState('');
  const [totalPrice, setTotalPrice] = useState(0);
  const [numberOfDays, setNumberOfDays] = useState(0);

  useEffect(() => {
    if (spotId) {
      fetchSpot(spotId);
    }
  }, [spotId]);

  useEffect(() => {
    if (dates && spot) {
      const [start, end] = dates;
      const days = end.diff(start, 'day');
      setNumberOfDays(days);
      setTotalPrice(days * spot.pricePerDay);
    }
  }, [dates, spot]);

  const fetchSpot = async (id: string) => {
    try {
      setLoading(true);
      const data = await spotsApi.getById(id);
      setSpot(data);
    } catch (error: any) {
      message.error('Failed to load spot details');
      navigate('/spots');
    } finally {
      setLoading(false);
    }
  };

  const handleBooking = async () => {
    if (!dates || !spot) {
      message.error('Please select dates');
      return;
    }

    if (guests < 1 || guests > spot.capacity) {
      message.error(`Guest count must be between 1 and ${spot.capacity}`);
      return;
    }

    const [checkIn, checkOut] = dates;

    try {
      setBookingLoading(true);

      // Check availability
      const availability = await bookingsApi.checkAvailability({
        spotId: spot.id,
        checkInDate: checkIn.format('YYYY-MM-DD'),
        checkOutDate: checkOut.format('YYYY-MM-DD'),
      });

      if (!availability.isAvailable) {
        message.error('Spot is not available for these dates');
        return;
      }

      // Create booking
      const booking = await bookingsApi.create({
        spotId: spot.id,
        checkInDate: checkIn.format('YYYY-MM-DD'),
        checkOutDate: checkOut.format('YYYY-MM-DD'),
        numberOfGuests: guests,
        specialRequests: specialRequests || undefined,
      });

      // Initiate payment
      const paymentOrder = await bookingsApi.initiatePayment(booking.id);

      // Load Razorpay script if not loaded
      if (!window.Razorpay) {
        const script = document.createElement('script');
        script.src = 'https://checkout.razorpay.com/v1/checkout.js';
        script.async = true;
        document.body.appendChild(script);
        await new Promise((resolve) => {
          script.onload = resolve;
        });
      }

      // Open Razorpay checkout
      const options = {
        key: paymentOrder.razorpayKeyId,
        amount: paymentOrder.amount,
        currency: paymentOrder.currency,
        name: 'Resorto',
        description: `Booking for ${spot.name}`,
        order_id: paymentOrder.orderId,
        handler: async (response: any) => {
          try {
            await bookingsApi.verifyPayment(booking.id, {
              razorpayOrderId: response.razorpay_order_id,
              razorpayPaymentId: response.razorpay_payment_id,
              razorpaySignature: response.razorpay_signature,
            });
            message.success('Booking confirmed successfully!');
            navigate('/my-bookings');
          } catch (error: any) {
            message.error('Payment verification failed');
          }
        },
        prefill: {
          name: '',
          email: '',
        },
        theme: {
          color: '#059669',
        },
      };

      const razorpay = new window.Razorpay(options);
      razorpay.open();
    } catch (error: any) {
      message.error(error.response?.data?.error || 'Failed to create booking');
    } finally {
      setBookingLoading(false);
    }
  };

  const disabledDate = (current: Dayjs) => {
    return current && current < dayjs().startOf('day');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spin size="large" />
      </div>
    );
  }

  if (!spot) {
    return null;
  }

  return (
    <div className="py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => navigate(`/spots/${spot.id}`)}
          className="mb-6 text-stone-600 hover:text-emerald-600 font-medium transition-colors"
        >
          ← Back to Spot Details
        </button>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Spot Summary */}
          <div className="glass-card p-6">
            <h2 className="text-2xl font-bold text-stone-900 mb-4">Booking Summary</h2>
            
            <div className="mb-4">
              <div className="h-48 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-lg flex items-center justify-center mb-4">
                {spot.images && spot.images[0] ? (
                  <img 
                    src={spot.images[0]} 
                    alt={spot.name}
                    className="w-full h-full object-cover rounded-lg"
                  />
                ) : (
                  <span className="text-6xl">{spot.spotType === 'picnic_area' ? '🏞️' : '🏨'}</span>
                )}
              </div>
              
              <h3 className="text-xl font-bold text-stone-900 mb-1">{spot.name}</h3>
              <p className="text-stone-600 text-sm mb-2">{spot.description}</p>
              <p className="text-emerald-600 font-semibold">₹{spot.pricePerDay} per day</p>
              <p className="text-stone-500 text-sm">Capacity: {spot.capacity} guests</p>
            </div>
          </div>

          {/* Booking Form */}
          <div className="glass-card p-6">
            <h2 className="text-2xl font-bold text-stone-900 mb-4">Booking Details</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-stone-900 mb-2">
                  Select Dates
                </label>
                <RangePicker
                  value={dates}
                  onChange={(values) => setDates(values as [Dayjs, Dayjs])}
                  disabledDate={disabledDate}
                  format="YYYY-MM-DD"
                  className="w-full"
                  size="large"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-stone-900 mb-2">
                  Number of Guests (Max: {spot.capacity})
                </label>
                <InputNumber
                  min={1}
                  max={spot.capacity}
                  value={guests}
                  onChange={(value) => setGuests(value || 1)}
                  className="w-full"
                  size="large"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-stone-900 mb-2">
                  Special Requests (Optional)
                </label>
                <textarea
                  value={specialRequests}
                  onChange={(e) => setSpecialRequests(e.target.value)}
                  className="input-field w-full h-24 resize-none"
                  placeholder="Any special requirements..."
                />
              </div>

              {dates && (
                <div className="pt-4 border-t border-stone-200">
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between text-stone-600">
                      <span>₹{spot.pricePerDay} × {numberOfDays} days</span>
                      <span>₹{totalPrice}</span>
                    </div>
                    <div className="flex justify-between text-xl font-bold text-stone-900">
                      <span>Total</span>
                      <span className="text-emerald-600">₹{totalPrice}</span>
                    </div>
                  </div>
                </div>
              )}

              <button
                onClick={handleBooking}
                disabled={!dates || bookingLoading}
                className="btn-primary"
              >
                {bookingLoading ? 'Processing...' : 'Proceed to Payment'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateBooking;
