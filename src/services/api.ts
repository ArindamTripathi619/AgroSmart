// API Service Layer for AgroSmart
// This replaces direct Supabase calls with backend API calls

// Use relative URL to work through nginx proxy in Docker, or direct URL in development
const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || '/api';

// Types for API requests and responses
export interface CropPredictionInput {
  soil_type: string;
  n_level: number;
  p_level: number;
  k_level: number;
  temperature: number;
  humidity: number;
  rainfall: number;
  ph_level: number;
  region: string;
}

export interface CropPredictionResult {
  predicted_crop: string;
  confidence_score: number;
  alternative_crops: { crop: string; score: number }[];
}

export interface FertilizerInput {
  crop_type: string;
  current_n: number;
  current_p: number;
  current_k: number;
  soil_ph: number;
  soil_type: string;
}

export interface FertilizerResult {
  recommended_fertilizer: string;
  npk_ratio: { n: number; p: number; k: number };
  quantity_per_hectare: number;
  application_timing: string;
  notes: string;
}

export interface YieldInput {
  crop_type: string;
  area_hectares: number;
  season: string;
  temperature: number;
  humidity: number;
  rainfall: number;
  soil_type: string;
  soil_ph: number;
  n_level: number;
  p_level: number;
  k_level: number;
}

export interface YieldResult {
  estimated_yield: number;
  confidence_interval: { lower: number; upper: number };
  regional_average: number;
  optimal_yield: number;
}

// API Error class
export class APIError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Generic fetch wrapper with error handling
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(
        errorData.message || `HTTP ${response.status}: ${response.statusText}`,
        response.status,
        errorData
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    // Network error or other issues
    throw new APIError(
      `Failed to connect to server. Please ensure the backend is running on ${API_BASE_URL}`,
      0,
      { originalError: error }
    );
  }
}

// Crop Prediction API
export async function predictCrop(
  data: CropPredictionInput
): Promise<CropPredictionResult> {
  return apiFetch<CropPredictionResult>('/predict-crop', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// Fertilizer Recommendation API
export async function recommendFertilizer(
  data: FertilizerInput
): Promise<FertilizerResult> {
  return apiFetch<FertilizerResult>('/recommend-fertilizer', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// Yield Estimation API
export async function estimateYield(
  data: YieldInput
): Promise<YieldResult> {
  return apiFetch<YieldResult>('/estimate-yield', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// Health check endpoint
export async function healthCheck(): Promise<{ status: string; message: string }> {
  return apiFetch<{ status: string; message: string }>('/health');
}

// Optional: Get statistics (if backend implements this)
export async function getStatistics(): Promise<{
  total_predictions: number;
  crops: number;
  fertilizers: number;
  yields: number;
}> {
  try {
    return apiFetch<{
      total_predictions: number;
      crops: number;
      fertilizers: number;
      yields: number;
    }>('/statistics');
  } catch (error) {
    // Return mock data if endpoint doesn't exist
    return {
      total_predictions: 0,
      crops: 0,
      fertilizers: 0,
      yields: 0,
    };
  }
}

// Check if backend is available
export async function isBackendAvailable(): Promise<boolean> {
  try {
    await healthCheck();
    return true;
  } catch {
    return false;
  }
}
