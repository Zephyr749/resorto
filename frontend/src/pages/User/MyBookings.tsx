import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { message, Spin, Modal } from 'antd';
import { bookingsApi } from '../../api/bookings';
import { BookingWithDetails } from '../../types';

const MyBookings = () => {
  const [bookings, setBookings] = useState<BookingWithDetails[]>([]);
  const [loading, setLoading] = useState(true);
  const [cancelLoading, setCancelLoading] = useState(false);
  const [selectedBooking, setSelectedBooking] = useState<BookingWithDetails | null>(null);

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const data = await bookingsApi.getMyBookings();
      setBookings(data);
    } catch (error: any) {
      message.error('Failed to load bookings');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId: string) => {
    try {
      setCancelLoading(true);
      await bookingsApi.cancel(bookingId);
      message.success('Booking cancelled successfully');
      setSelectedBooking(null);
      fetchBookings();
    } catch (error: any) {
      message.error(error.response?.data?.error || 'Failed to cancel booking');
    } finally {
      setCancelLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed':
        return 'bg-emerald-100 text-emerald-700';
      case 'cancelled':
        return 'bg-red-100 text-red-700';
      case 'completed':
        return 'bg-blue-100 text-blue-700';
      default:
        return 'bg-stone-100 text-stone-700';
    }
  };

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div className="py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-stone-900 mb-8">My Bookings</h1>

        {bookings.length === 0 ? (
          <div className="glass-card p-12 text-center">
            <div className="text-6xl mb-6">📅</div>
            <h2 className="text-2xl font-semibold text-stone-900 mb-4">
              No Bookings Yet
            </h2>
            <p className="text-stone-600 mb-8">
              Start exploring our spots and make your first reservation.
            </p>
            <Link
              to="/spots"
              className="inline-block px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-semibold rounded-lg hover:from-emerald-500 hover:to-teal-500 transition-all shadow-md"
            >
              Browse Spots
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {bookings.map((booking) => (
              <div key={booking.id} className="glass-card p-6">
                <div className="flex flex-col md:flex-row md:items-start md:justify-between">
                  {/* Booking Info */}
                  <div className="flex-1 mb-4 md:mb-0">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-xl font-bold text-stone-900 mb-1">
                          {booking.spot?.name || 'Spot'}
                        </h3>
                        <span className={`inline-block px-3 py-1 text-sm font-semibold rounded-full ${getStatusColor(booking.status)}`}>
                          {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                        </span>
                      </div>
                    </div>

                    <div className="space-y-2 text-stone-600">
                      <p>
                        <span className="font-semibold">Check-in:</span> {formatDate(booking.checkInDate)}
                      </p>
                      <p>
                        <span className="font-semibold">Check-out:</span> {formatDate(booking.checkOutDate)}
                      </p>
                      <p>
                        <span className="font-semibold">Guests:</span> {booking.numberOfGuests}
                      </p>
                      <p>
                        <span className="font-semibold">Total:</span> ₹{booking.totalAmount}
                      </p>
                      {booking.paymentStatus && (
                        <p>
                          <span className="font-semibold">Payment:</span>{' '}
                          <span className={booking.paymentStatus === 'paid' ? 'text-emerald-600' : 'text-stone-600'}>
                            {booking.paymentStatus.charAt(0).toUpperCase() + booking.paymentStatus.slice(1)}
                          </span>
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col gap-2">
                    {booking.status === 'confirmed' && (
                      <button
                        onClick={() => setSelectedBooking(booking)}
                        className="px-4 py-2 bg-red-100 text-red-700 font-semibold rounded-lg hover:bg-red-200 transition-colors"
                      >
                        Cancel Booking
                      </button>
                    )}
                    <Link
                      to={`/spots/${booking.spot?.id}`}
                      className="px-4 py-2 bg-stone-100 text-stone-700 font-semibold rounded-lg hover:bg-stone-200 transition-colors text-center"
                    >
                      View Spot
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Cancel Confirmation Modal */}
        <Modal
          title="Cancel Booking"
          open={!!selectedBooking}
          onCancel={() => setSelectedBooking(null)}
          footer={null}
        >
          <div className="py-4">
            <p className="text-stone-600 mb-6">
              Are you sure you want to cancel this booking? Refund will be processed according to our refund policy.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => selectedBooking && handleCancelBooking(selectedBooking.id)}
                disabled={cancelLoading}
                className="btn-primary"
              >
                {cancelLoading ? 'Cancelling...' : 'Yes, Cancel Booking'}
              </button>
              <button
                onClick={() => setSelectedBooking(null)}
                className="flex-1 px-4 py-3 rounded-lg bg-stone-100 text-stone-700 font-semibold hover:bg-stone-200 transition-colors"
              >
                Keep Booking
              </button>
            </div>
          </div>
        </Modal>
      </div>
    </div>
  );
};

export default MyBookings;
