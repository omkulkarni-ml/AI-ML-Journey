import { useState } from 'react'

const PredictionForm = ({ features, selectedFeatures, onSubmit, onBack }) => {
  const [formData, setFormData] = useState({})
  const [errors, setErrors] = useState({})

  const handleChange = (featureName, value, featureInfo) => {
    let processedValue = value
    if (featureInfo.type === 'numeric') {
      processedValue = parseFloat(value) || 0
    }

    setFormData(prev => ({
      ...prev,
      [featureName]: processedValue
    }))

    if (errors[featureName]) {
      setErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[featureName]
        return newErrors
      })
    }
  }

  const validateForm = () => {
    const newErrors = {}
    selectedFeatures.forEach(featureName => {
      const featureInfo = features.all_features[featureName]
      const value = formData[featureName]

      if (value === undefined || value === '') {
        newErrors[featureName] = 'Required'
      } else if (featureInfo.type === 'numeric') {
        const numValue = parseFloat(value)
        if (isNaN(numValue)) {
          newErrors[featureName] = 'Invalid number'
        } else if (numValue < featureInfo.min || numValue > featureInfo.max) {
          newErrors[featureName] = `${featureInfo.min}-${featureInfo.max}`
        }
      }
    })

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validateForm()) {
      onSubmit(formData)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6 pt-20">
      <div className="w-full max-w-lg animate-fade-in">
        {/* Header */}
        <div className="text-center mb-8">
          <button
            onClick={onBack}
            className="text-white/40 hover:text-white text-sm mb-4 transition-colors"
          >
            Back
          </button>
          <h2 className="text-2xl font-semibold text-white mb-2">Enter Data</h2>
          <p className="text-white/40 text-sm">
            Provide student information
          </p>
        </div>

        <form onSubmit={handleSubmit} className="glass-card">
          <div className="space-y-5">
            {selectedFeatures.map(featureName => {
              const featureInfo = features.all_features[featureName]
              
              return (
                <div key={featureName} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-white/80">
                      {featureName}
                    </label>
                    {errors[featureName] && (
                      <span className="text-xs text-red-400">{errors[featureName]}</span>
                    )}
                  </div>
                  
                  {featureInfo.type === 'numeric' ? (
                    <div className="space-y-3">
                      <input
                        type="number"
                        step="any"
                        value={formData[featureName] || ''}
                        onChange={(e) => handleChange(featureName, e.target.value, featureInfo)}
                        placeholder={`${featureInfo.min} - ${featureInfo.max}`}
                        className={`dark-input ${errors[featureName] ? 'border-red-500/50' : ''}`}
                      />
                      <input
                        type="range"
                        min={featureInfo.min}
                        max={featureInfo.max}
                        step="0.5"
                        value={formData[featureName] || featureInfo.default}
                        onChange={(e) => handleChange(featureName, e.target.value, featureInfo)}
                        className="dark-range"
                      />
                      <div className="flex justify-between text-xs text-white/30">
                        <span>{featureInfo.min}</span>
                        <span>{featureInfo.max}</span>
                      </div>
                    </div>
                  ) : (
                    <select
                      value={formData[featureName] || featureInfo.default}
                      onChange={(e) => handleChange(featureName, e.target.value, featureInfo)}
                      className="dark-select"
                    >
                      {featureInfo.options.map(option => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  )}
                </div>
              )
            })}
          </div>

          <div className="mt-8">
            <button
              type="submit"
              className="btn-primary w-full"
            >
              Predict
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default PredictionForm
