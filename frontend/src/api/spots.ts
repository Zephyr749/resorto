import apiClient from './client';
import { API_ENDPOINTS } from '../config/api';
import { Spot, ApiResponse } from '../types';

export const spotsApi = {
  getAll: async (spotType?: string): Promise<Spot[]> => {
    const params = spotType ? { spotType } : {};
    const { data } = await apiClient.get<ApiResponse<{ spots: Spot[] }>>(
      API_ENDPOINTS.SPOTS,
      { params }
    );
    return data.data!.spots;
  },

  getById: async (id: string): Promise<Spot> => {
    const { data } = await apiClient.get<ApiResponse<{ spot: Spot }>>(
      API_ENDPOINTS.SPOT_DETAIL(id)
    );
    return data.data!.spot;
  },
};
