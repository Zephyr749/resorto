import apiClient from './client';
import { API_ENDPOINTS } from '../config/api';
import { LoginCredentials, RegisterData, LoginResponse, User, ApiResponse } from '../types';

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
    const { data } = await apiClient.post<ApiResponse<LoginResponse>>(
      API_ENDPOINTS.LOGIN,
      credentials
    );
    return data.data!;
  },

  register: async (userData: RegisterData): Promise<LoginResponse> => {
    const { data } = await apiClient.post<ApiResponse<LoginResponse>>(
      API_ENDPOINTS.REGISTER,
      userData
    );
    return data.data!;
  },

  getProfile: async (): Promise<User> => {
    const { data } = await apiClient.get<ApiResponse<{ user: User }>>(
      API_ENDPOINTS.PROFILE
    );
    return data.data!.user;
  },

  updateProfile: async (userData: { firstName: string; lastName: string }): Promise<User> => {
    const { data } = await apiClient.put<ApiResponse<{ user: User }>>(
      API_ENDPOINTS.PROFILE,
      userData
    );
    return data.data!.user;
  },

  changePassword: async (passwords: { currentPassword: string; newPassword: string }): Promise<void> => {
    await apiClient.post(API_ENDPOINTS.CHANGE_PASSWORD, passwords);
  },
};
