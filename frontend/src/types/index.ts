export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  fullName: string;
  role: 'user' | 'admin';
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
}

export interface LoginResponse {
  user: User;
  token: string;
}

export interface Spot {
  id: string;
  name: string;
  description: string;
  spotType: 'picnic_area' | 'room';
  capacity: number;
  pricePerDay: number;
  amenities: string[];
  images: string[];
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface SpotCreate {
  name: string;
  description: string;
  spotType: 'picnic_area' | 'room';
  capacity: number;
  pricePerDay: number;
  amenities: string[];
  images: string[];
}

export interface Booking {
  id: string;
  userId: string;
  spotId: string;
  checkInDate: string;
  checkOutDate: string;
  numberOfGuests: number;
  specialRequests?: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  totalAmount: number;
  paymentStatus: 'pending' | 'paid' | 'failed' | 'refunded';
  paymentId?: string;
  createdAt: string;
  updatedAt: string;
}

export interface BookingWithDetails extends Booking {
  spot: Spot;
  userName: string;
  userEmail: string;
}

export interface BookingCreate {
  spotId: string;
  checkInDate: string;
  checkOutDate: string;
  numberOfGuests: number;
  specialRequests?: string;
}

export interface AvailabilityCheck {
  spotId: string;
  checkInDate: string;
  checkOutDate: string;
}

export interface AvailabilityResponse {
  spotId: string;
  isAvailable: boolean;
  conflictingBookings: string[];
}

export interface PaymentOrder {
  orderId: string;
  amount: number;
  currency: string;
  razorpayKeyId: string;
}

export interface AdminCancelBooking {
  reason: string;
  refundOption: 'auto' | 'full' | 'partial' | 'none';
  refundAmount?: number;
}

export interface RefundInfo {
  refundAmount: number;
  refundPercentage: number;
  daysUntilCheckIn: number;
  refundProcessed: boolean;
  refundOption: string;
  refundId?: string;
  refundError?: string;
}

export interface BookingStats {
  totalBookings: number;
  confirmedBookings: number;
  pendingBookings: number;
  cancelledBookings: number;
  totalRevenue: number;
  todayBookings: number;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message: string;
}
