/**
 * Authentication store using Zustand
 */
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from '../services/api'

const useAuthStore = create(
  persist(
    (set, get) => ({
      // State
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
      onboardingStep: 0,
      onboardingCompleted: false,

      // Actions
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      
      setLoading: (isLoading) => set({ isLoading }),
      
      setError: (error) => set({ error }),
      
      clearError: () => set({ error: null }),

      // Login
      login: async (email, password) => {
        set({ isLoading: true, error: null })
        try {
          const response = await api.login(email, password)
          const { user, tokens } = response.data.data
          
          // Store tokens
          localStorage.setItem('access_token', tokens.access_token)
          localStorage.setItem('refresh_token', tokens.refresh_token)
          
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
            onboardingStep: user.onboarding_step || 0,
            onboardingCompleted: user.onboarding_completed || false
          })
          
          return { success: true, user }
        } catch (error) {
          const message = error.response?.data?.error || 'Login failed'
          set({ isLoading: false, error: message })
          return { success: false, error: message }
        }
      },

      // Register
      register: async (userData) => {
        set({ isLoading: true, error: null })
        try {
          const response = await api.register(userData)
          set({ isLoading: false })
          return { success: true, data: response.data }
        } catch (error) {
          console.error('Registration error:', error)
          let message = 'Registration failed'
          if (error.response?.data?.error) {
            message = error.response.data.error
          } else if (error.message === 'Network Error') {
            message = 'Network error: Cannot connect to server. Please check your connection or try again later.'
          } else if (error.code === 'ERR_CORS') {
            message = 'CORS error: Server configuration issue. Please contact support.'
          } else if (error.message) {
            message = `Registration failed: ${error.message}`
          }
          set({ isLoading: false, error: message })
          return { success: false, error: message }
        }
      },

      // Logout
      logout: async () => {
        try {
          await api.logout()
        } catch (error) {
          console.error('Logout error:', error)
        } finally {
          // Clear all auth data
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
            onboardingStep: 0,
            onboardingCompleted: false
          })
        }
      },

      // Refresh token
      refreshToken: async () => {
        try {
          const response = await api.refreshToken()
          const { access_token } = response.data.data
          localStorage.setItem('access_token', access_token)
          return { success: true }
        } catch (error) {
          // Token refresh failed, logout user
          get().logout()
          return { success: false, error: 'Session expired' }
        }
      },

      // Fetch current user
      fetchCurrentUser: async () => {
        try {
          const response = await api.getCurrentUser()
          const { user } = response.data.data
          set({
            user,
            isAuthenticated: true,
            onboardingStep: user.onboarding_step || 0,
            onboardingCompleted: user.onboarding_completed || false
          })
          return { success: true, user }
        } catch (error) {
          // If 401, token is invalid
          if (error.response?.status === 401) {
            get().logout()
          }
          return { success: false, error: error.message }
        }
      },

      // Update onboarding
      updateOnboarding: async (data) => {
        try {
          const response = await api.updateOnboarding(data)
          const { user } = response.data.data
          set({
            user,
            onboardingStep: user.onboarding_step,
            onboardingCompleted: user.onboarding_completed
          })
          return { success: true }
        } catch (error) {
          return { success: false, error: error.message }
        }
      },

      // Update user profile
      updateProfile: async (profileData) => {
        set({ isLoading: true })
        try {
          const response = await api.updateProfile(profileData)
          const { user } = response.data.data
          set({ user, isLoading: false })
          return { success: true, user }
        } catch (error) {
          set({ isLoading: false })
          return { success: false, error: error.message }
        }
      },

      // Change password
      changePassword: async (currentPassword, newPassword) => {
        try {
          await api.changePassword(currentPassword, newPassword)
          return { success: true }
        } catch (error) {
          const message = error.response?.data?.error || 'Failed to change password'
          return { success: false, error: message }
        }
      }
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        onboardingStep: state.onboardingStep,
        onboardingCompleted: state.onboardingCompleted
      })
    }
  )
)

export default useAuthStore
