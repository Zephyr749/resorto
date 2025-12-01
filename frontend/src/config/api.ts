export const API_BASE_URL = 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Auth
  REGISTER: '/auth/register',
  LOGIN: '/auth/login',
  PROFILE: '/auth/profile',
  CHANGE_PASSWORD: '/auth/change-password',

  // Public Spots
  SPOTS: '/spots',
  SPOT_DETAIL: (id: string) => `/spots/${id}`,
  CHECK_AVAILABILITY: '/bookings/check-availability',

  // User Bookings
  BOOKINGS: '/bookings',
  MY_BOOKINGS: '/bookings/my-bookings',
  BOOKING_DETAIL: (id: string) => `/bookings/${id}`,
  CANCEL_BOOKING: (id: string) => `/bookings/${id}/cancel`,
  
  // Payments
  PAY_BOOKING: (id: string) => `/bookings/${id}/pay`,
  VERIFY_PAYMENT: (id: string) => `/bookings/${id}/verify-payment`,

  // Admin - Spots
  ADMIN_SPOTS: '/admin/spots',
  ADMIN_SPOT_DETAIL: (id: string) => `/admin/spots/${id}`,

  // Admin - Bookings
  ADMIN_BOOKINGS: '/admin/bookings',
  ADMIN_BOOKING_DETAIL: (id: string) => `/admin/bookings/${id}`,
  ADMIN_CANCEL_BOOKING: (id: string) => `/admin/bookings/${id}/cancel`,
  ADMIN_REFUND: (id: string) => `/admin/bookings/${id}/refund`,
  ADMIN_STATS: '/admin/bookings/stats/overview',
};
