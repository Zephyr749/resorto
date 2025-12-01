import { useEffect, useState } from 'react';
import { message, Spin, Modal, Form, Input, Select, InputNumber } from 'antd';
import { adminApi } from '../../api/admin';
import { BookingWithDetails } from '../../types';

const { TextArea } = Input;
const { Option } = Select;

const BookingManagement = () => {
  const [bookings, setBookings] = useState<BookingWithDetails[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'confirmed' | 'pending' | 'cancelled'>('all');
  const [cancelModalVisible, setCancelModalVisible] = useState(false);
  const [selectedBooking, setSelectedBooking] = useState<BookingWithDetails | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const data = await adminApi.getAllBookings();
      setBookings(data);
    } catch (error: any) {
      message.error('Failed to load bookings');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (values: any) => {
    if (!selectedBooking) return;

    try {
      const cancelData = {
        reason: values.reason,
        refundOption: values.refundOption,
        refundAmount: values.refundOption === 'partial' ? values.refundAmount : undefined,
      };

      await adminApi.cancelBooking(selectedBooking.id, cancelData);
      message.success('Booking cancelled successfully');
      setCancelModalVisible(false);
      setSelectedBooking(null);
      form.resetFields();
      fetchBookings();
    } catch (error: any) {
      message.error(error.response?.data?.error || 'Failed to cancel booking');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed':
        return 'bg-emerald-100 text-emerald-700';
      case 'pending':
        return 'bg-amber-100 text-amber-700';
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

  const filteredBookings = bookings.filter(booking => {
    if (filter === 'all') return true;
    return booking.status === filter;
  });

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div className="py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-stone-900 mb-8">Manage Bookings</h1>

        {/* Filter Tabs */}
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setFilter('all')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              filter === 'all'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md'
                : 'bg-white text-stone-700 hover:bg-stone-50'
            }`}
          >
            All ({bookings.length})
          </button>
          <button
            onClick={() => setFilter('confirmed')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              filter === 'confirmed'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md'
                : 'bg-white text-stone-700 hover:bg-stone-50'
            }`}
          >
            Confirmed ({bookings.filter(b => b.status === 'confirmed').length})
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              filter === 'pending'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md'
                : 'bg-white text-stone-700 hover:bg-stone-50'
            }`}
          >
            Pending ({bookings.filter(b => b.status === 'pending').length})
          </button>
          <button
            onClick={() => setFilter('cancelled')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              filter === 'cancelled'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md'
                : 'bg-white text-stone-700 hover:bg-stone-50'
            }`}
          >
            Cancelled ({bookings.filter(b => b.status === 'cancelled').length})
          </button>
        </div>

        {/* Bookings List */}
        <div className="space-y-4">
          {filteredBookings.length === 0 ? (
            <div className="glass-card p-12 text-center">
              <div className="text-6xl mb-6">📋</div>
              <h2 className="text-2xl font-semibold text-stone-900 mb-4">
                No Bookings Found
              </h2>
              <p className="text-stone-600">
                {filter === 'all' ? 'No bookings in the system yet.' : `No ${filter} bookings.`}
              </p>
            </div>
          ) : (
            filteredBookings.map((booking) => (
              <div key={booking.id} className="glass-card p-6">
                <div className="grid md:grid-cols-4 gap-4">
                  {/* Booking Info */}
                  <div className="md:col-span-2">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-lg font-bold text-stone-900 mb-1">
                          {booking.spot?.name || 'Spot'}
                        </h3>
                        <p className="text-sm text-stone-600">
                          {booking.userName} ({booking.userEmail})
                        </p>
                      </div>
                      <span className={`px-3 py-1 text-sm font-semibold rounded-full ${getStatusColor(booking.status)}`}>
                        {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                      </span>
                    </div>
                    <div className="space-y-1 text-sm text-stone-600">
                      <p><span className="font-semibold">Check-in:</span> {formatDate(booking.checkInDate)}</p>
                      <p><span className="font-semibold">Check-out:</span> {formatDate(booking.checkOutDate)}</p>
                      <p><span className="font-semibold">Guests:</span> {booking.numberOfGuests}</p>
                    </div>
                  </div>

                  {/* Payment Info */}
                  <div>
                    <p className="text-sm text-stone-600 mb-1">Payment</p>
                    <p className="text-2xl font-bold text-emerald-600 mb-2">₹{booking.totalAmount}</p>
                    <span className={`inline-block px-2 py-1 text-xs font-semibold rounded ${
                      booking.paymentStatus === 'paid'
                        ? 'bg-emerald-100 text-emerald-700'
                        : booking.paymentStatus === 'refunded'
                        ? 'bg-blue-100 text-blue-700'
                        : 'bg-amber-100 text-amber-700'
                    }`}>
                      {booking.paymentStatus.toUpperCase()}
                    </span>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col gap-2">
                    {booking.status === 'confirmed' && (
                      <button
                        onClick={() => {
                          setSelectedBooking(booking);
                          setCancelModalVisible(true);
                        }}
                        className="px-4 py-2 bg-red-100 text-red-700 font-semibold rounded-lg hover:bg-red-200 transition-colors"
                      >
                        Cancel Booking
                      </button>
                    )}
                    <a
                      href={`/spots/${booking.spot?.id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-stone-100 text-stone-700 font-semibold rounded-lg hover:bg-stone-200 transition-colors text-center"
                    >
                      View Spot
                    </a>
                  </div>
                </div>

                {booking.specialRequests && (
                  <div className="mt-4 pt-4 border-t border-stone-200">
                    <p className="text-sm font-semibold text-stone-700 mb-1">Special Requests:</p>
                    <p className="text-sm text-stone-600">{booking.specialRequests}</p>
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Cancel Modal */}
        <Modal
          title="Cancel Booking - Admin"
          open={cancelModalVisible}
          onCancel={() => {
            setCancelModalVisible(false);
            setSelectedBooking(null);
            form.resetFields();
          }}
          footer={null}
          width={600}
        >
          <Form
            form={form}
            layout="vertical"
            onFinish={handleCancelBooking}
            className="mt-4"
          >
            <Form.Item
              name="reason"
              label={<span className="text-sm font-semibold text-stone-900">Cancellation Reason</span>}
              rules={[{ required: true, message: 'Please enter reason' }]}
            >
              <TextArea rows={3} className="input-field" placeholder="Reason for cancellation..." />
            </Form.Item>

            <Form.Item
              name="refundOption"
              label={<span className="text-sm font-semibold text-stone-900">Refund Option</span>}
              rules={[{ required: true, message: 'Please select refund option' }]}
              initialValue="auto"
            >
              <Select>
                <Option value="auto">Auto (Based on Policy)</Option>
                <Option value="full">Full Refund</Option>
                <Option value="partial">Partial Refund</Option>
                <Option value="none">No Refund</Option>
              </Select>
            </Form.Item>

            <Form.Item
              noStyle
              shouldUpdate={(prevValues, currentValues) => prevValues.refundOption !== currentValues.refundOption}
            >
              {({ getFieldValue }) =>
                getFieldValue('refundOption') === 'partial' ? (
                  <Form.Item
                    name="refundAmount"
                    label={<span className="text-sm font-semibold text-stone-900">Refund Amount (₹)</span>}
                    rules={[{ required: true, message: 'Please enter refund amount' }]}
                  >
                    <InputNumber
                      min={0}
                      max={selectedBooking?.totalAmount}
                      className="w-full"
                      placeholder={`Max: ₹${selectedBooking?.totalAmount || 0}`}
                    />
                  </Form.Item>
                ) : null
              }
            </Form.Item>

            <div className="flex gap-3">
              <button type="submit" className="btn-primary">
                Cancel Booking & Process Refund
              </button>
              <button
                type="button"
                onClick={() => {
                  setCancelModalVisible(false);
                  setSelectedBooking(null);
                  form.resetFields();
                }}
                className="flex-1 px-4 py-3 rounded-lg bg-stone-100 text-stone-700 font-semibold hover:bg-stone-200 transition-colors"
              >
                Close
              </button>
            </div>
          </Form>
        </Modal>
      </div>
    </div>
  );
};

export default BookingManagement;
