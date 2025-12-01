import apiClient from './client';
import { API_ENDPOINTS } from '../config/api';
import {
  Spot,
  SpotCreate,
  BookingWithDetails,
  BookingStats,
  AdminCancelBooking,
  Booking,
  RefundInfo,
  ApiResponse,
} from '../types';

export const adminApi = {
  // Spot Management
  createSpot: async (spot: SpotCreate): Promise<Spot> => {
    const { data } = await apiClient.post<ApiResponse<{ spot: Spot }>>(
      API_ENDPOINTS.ADMIN_SPOTS,
      spot
    );
    return data.data!.spot;
  },

  updateSpot: async (id: string, spot: Partial<SpotCreate>): Promise<Spot> => {
    const { data } = await apiClient.put<ApiResponse<{ spot: Spot }>>(
      API_ENDPOINTS.ADMIN_SPOT_DETAIL(id),
      spot
    );
    return data.data!.spot;
  },

  deleteSpot: async (id: string): Promise<void> => {
    await apiClient.delete(API_ENDPOINTS.ADMIN_SPOT_DETAIL(id));
  },

  getAllSpots: async (isActive?: boolean): Promise<Spot[]> => {
    const params = isActive !== undefined ? { isActive } : {};
    const { data } = await apiClient.get<ApiResponse<{ spots: Spot[] }>>(
      API_ENDPOINTS.ADMIN_SPOTS,
      { params }
    );
    return data.data!.spots;
  },

  // Booking Management
  getAllBookings: async (status?: string): Promise<BookingWithDetails[]> => {
    const params = status ? { status } : {};
    const { data } = await apiClient.get<ApiResponse<{ bookings: BookingWithDetails[] }>>(
      API_ENDPOINTS.ADMIN_BOOKINGS,
      { params }
    );
    return data.data!.bookings;
  },

  getBookingById: async (id: string): Promise<BookingWithDetails> => {
    const { data } = await apiClient.get<ApiResponse<{ booking: BookingWithDetails }>>(
      API_ENDPOINTS.ADMIN_BOOKING_DETAIL(id)
    );
    return data.data!.booking;
  },

  cancelBooking: async (
    id: string,
    cancelData: AdminCancelBooking
  ): Promise<{ booking: Booking; refund: RefundInfo | null; reason: string }> => {
    const { data } = await apiClient.post<
      ApiResponse<{ booking: Booking; refund: RefundInfo | null; reason: string }>
    >(API_ENDPOINTS.ADMIN_CANCEL_BOOKING(id), cancelData);
    return data.data!;
  },

  refundBooking: async (
    id: string,
    refundData: { reason: string; refundAmount?: number }
  ): Promise<any> => {
    const { data } = await apiClient.post(
      API_ENDPOINTS.ADMIN_REFUND(id),
      refundData
    );
    return data.data;
  },

  getStats: async (): Promise<BookingStats> => {
    const { data } = await apiClient.get<ApiResponse<{ stats: BookingStats }>>(
      API_ENDPOINTS.ADMIN_STATS
    );
    return data.data!.stats;
  },
};
