import apiClient from './client';
import { API_ENDPOINTS } from '../config/api';
import {
  Booking,
  BookingWithDetails,
  BookingCreate,
  AvailabilityCheck,
  AvailabilityResponse,
  PaymentOrder,
  RefundInfo,
  ApiResponse,
} from '../types';

export const bookingsApi = {
  checkAvailability: async (check: AvailabilityCheck): Promise<AvailabilityResponse> => {
    const { data } = await apiClient.post<ApiResponse<AvailabilityResponse>>(
      API_ENDPOINTS.CHECK_AVAILABILITY,
      check
    );
    return data.data!;
  },

  create: async (booking: BookingCreate): Promise<Booking> => {
    const { data} = await apiClient.post<ApiResponse<{ booking: Booking }>>(
      API_ENDPOINTS.BOOKINGS,
      booking
    );
    return data.data!.booking;
  },

  getMyBookings: async (): Promise<BookingWithDetails[]> => {
    const { data } = await apiClient.get<ApiResponse<{ bookings: BookingWithDetails[] }>>(
      API_ENDPOINTS.MY_BOOKINGS
    );
    return data.data!.bookings;
  },

  getById: async (id: string): Promise<BookingWithDetails> => {
    const { data } = await apiClient.get<ApiResponse<{ booking: BookingWithDetails }>>(
      API_ENDPOINTS.BOOKING_DETAIL(id)
    );
    return data.data!.booking;
  },

  cancel: async (id: string): Promise<{ booking: Booking; refund: RefundInfo | null }> => {
    const { data } = await apiClient.post<ApiResponse<{ booking: Booking; refund: RefundInfo | null }>>(
      API_ENDPOINTS.CANCEL_BOOKING(id)
    );
    return data.data!;
  },

  initiatePayment: async (id: string): Promise<PaymentOrder> => {
    const { data } = await apiClient.post<ApiResponse<PaymentOrder>>(
      API_ENDPOINTS.PAY_BOOKING(id)
    );
    return data.data!;
  },

  verifyPayment: async (
    id: string,
    paymentData: {
      razorpayOrderId: string;
      razorpayPaymentId: string;
      razorpaySignature: string;
    }
  ): Promise<any> => {
    const { data } = await apiClient.post(
      API_ENDPOINTS.VERIFY_PAYMENT(id),
      paymentData
    );
    return data.data;
  },
};
