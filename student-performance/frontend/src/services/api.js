import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If 401 and not already retrying
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) {
          throw new Error('No refresh token')
        }

        // Try to refresh token
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {}, {
          headers: {
            Authorization: `Bearer ${refreshToken}`
          }
        })

        const { access_token } = response.data.data
        localStorage.setItem('access_token', access_token)

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        // Refresh failed, clear tokens
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

const api = {
  // Health check
  healthCheck: () => apiClient.get('/health'),

  // Model info
  getModelInfo: () => apiClient.get('/model/info'),

  // Features
  getFeatures: () => apiClient.get('/features'),
  getNumericFeatures: () => apiClient.get('/features/numeric'),
  getCategoricalFeatures: () => apiClient.get('/features/categorical'),
  getDefaultFeatures: () => apiClient.get('/features/defaults'),

  // Predictions
  predict: (data) => apiClient.post('/predict', data),
  validateInput: (data) => apiClient.post('/predict/validate', data),

  // Authentication
  login: (email, password) => apiClient.post('/auth/login', { email, password }),
  register: (userData) => apiClient.post('/auth/register', userData),
  logout: () => apiClient.post('/auth/logout'),
  refreshToken: () => {
    const refreshToken = localStorage.getItem('refresh_token')
    return axios.post(`${API_BASE_URL}/auth/refresh`, {}, {
      headers: {
        Authorization: `Bearer ${refreshToken}`
      }
    })
  },
  getCurrentUser: () => apiClient.get('/auth/me'),
  updateOnboarding: (data) => apiClient.put('/auth/onboarding', data),
  changePassword: (currentPassword, newPassword) => 
    apiClient.put('/auth/change-password', { current_password: currentPassword, new_password: newPassword }),

  // User profile
  updateProfile: (data) => apiClient.put('/auth/profile', data),

  // Prediction history
  getPredictionHistory: () => apiClient.get('/predictions/history'),
  getPredictionById: (id) => apiClient.get(`/predictions/${id}`),
  deletePrediction: (id) => apiClient.delete(`/predictions/${id}`)
}

export default api
