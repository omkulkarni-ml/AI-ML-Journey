/**
 * Dashboard Page
 * Main application dashboard with navigation
 */
import { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import useAuthStore from '../store/authStore'
import Navbar from '../components/Navbar'
import FeatureSelector from '../components/FeatureSelector'
import PredictionForm from '../components/PredictionForm'
import ResultDisplay from '../components/ResultDisplay'
import LoadingSpinner from '../components/LoadingSpinner'
import api from '../services/api'
import { useState } from 'react'

const DashboardContent = () => {
  const [view, setView] = useState('select')
  const [features, setFeatures] = useState(null)
  const [selectedFeatures, setSelectedFeatures] = useState([])
  const [formData, setFormData] = useState({})
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [apiStatus, setApiStatus] = useState('checking')

  useEffect(() => {
    checkApiHealth()
  }, [])

  const checkApiHealth = async () => {
    setApiStatus('checking')
    // Try multiple times with delay for Render free tier wake-up
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        const response = await api.healthCheck()
        if (response.data.success) {
          setApiStatus('connected')
          return
        }
      } catch (err) {
        console.log(`Health check attempt ${attempt} failed, retrying...`)
        if (attempt < 3) {
          // Wait 15 seconds before retry (Render free tier wake-up time)
          await new Promise(resolve => setTimeout(resolve, 15000))
        }
      }
    }
    setApiStatus('disconnected')
  }

  const loadFeatures = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.getFeatures()
      if (response.data.success) {
        setFeatures(response.data.data)
        setSelectedFeatures(response.data.data.default_features || ['studytime', 'failures', 'absences'])
      }
    } catch (err) {
      setError('Failed to connect to API')
    } finally {
      setLoading(false)
    }
  }

  const handleFeatureSelect = (featureName, isSelected) => {
    if (isSelected) {
      setSelectedFeatures(prev => [...prev, featureName])
    } else {
      setSelectedFeatures(prev => prev.filter(f => f !== featureName))
    }
  }

  const handleFormSubmit = async (data) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.predict({
        features: data,
        selected_features: selectedFeatures
      })
      if (response.data.success) {
        setPrediction(response.data.data)
        setFormData(data)
        setView('result')
      } else {
        setError(response.data.error || 'Prediction failed')
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to make prediction')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setView('select')
    setPrediction(null)
    setFormData({})
    setError(null)
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <Navbar apiStatus={apiStatus} />
      
      {loading && <LoadingSpinner />}
      
      {error && (
        <div className="fixed top-20 left-1/2 -translate-x-1/2 px-4 py-2 bg-red-500/20 border border-red-500/30 text-red-400 text-sm rounded-lg z-50">
          {error}
        </div>
      )}

      {view === 'select' && (
        <FeatureSelector
          features={features}
          selectedFeatures={selectedFeatures}
          onFeatureSelect={handleFeatureSelect}
          onLoadFeatures={loadFeatures}
          onProceed={() => setView('form')}
        />
      )}

      {view === 'form' && features && (
        <PredictionForm
          features={features}
          selectedFeatures={selectedFeatures}
          onSubmit={handleFormSubmit}
          onBack={() => setView('select')}
        />
      )}

      {view === 'result' && prediction && (
        <ResultDisplay
          prediction={prediction}
          selectedFeatures={selectedFeatures}
          formData={formData}
          onReset={handleReset}
        />
      )}
    </div>
  )
}

const DashboardPage = () => {
  const { isAuthenticated, fetchCurrentUser } = useAuthStore()

  useEffect(() => {
    if (isAuthenticated) {
      fetchCurrentUser()
    }
  }, [isAuthenticated, fetchCurrentUser])

  return <DashboardContent />
}

export default DashboardPage
