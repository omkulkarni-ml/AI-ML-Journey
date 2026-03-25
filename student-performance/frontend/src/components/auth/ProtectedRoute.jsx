/**
 * Protected Route Component
 * Redirects to login if user is not authenticated
 */
import { useEffect, useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import useAuthStore from '../../store/authStore'
import LoadingSpinner from '../LoadingSpinner'

const ProtectedRoute = ({ children, requireOnboarding = true }) => {
  const { isAuthenticated, onboardingCompleted, fetchCurrentUser } = useAuthStore()
  const [isChecking, setIsChecking] = useState(true)
  const location = useLocation()

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token')
      if (token && !isAuthenticated) {
        await fetchCurrentUser()
      }
      setIsChecking(false)
    }
    checkAuth()
  }, [isAuthenticated, fetchCurrentUser])

  if (isChecking) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  // Check if onboarding is required and not completed
  if (requireOnboarding && !onboardingCompleted && location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />
  }

  return children
}

export default ProtectedRoute
