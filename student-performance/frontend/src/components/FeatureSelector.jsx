import { useState } from 'react'

const FeatureSelector = ({ features, selectedFeatures, onFeatureSelect, onLoadFeatures, onProceed }) => {
  const [activeTab, setActiveTab] = useState('all')

  if (!features) {
    return (
      <div className="min-h-screen flex items-center justify-center px-6">
        <div className="text-center max-w-md animate-fade-in">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Student Performance</h1>
          <p className="text-white/50 mb-8 text-sm">
            Predict academic success using machine learning
          </p>
          <button
            onClick={onLoadFeatures}
            className="btn-primary"
          >
            Get Started
          </button>
        </div>
      </div>
    )
  }

  const filteredFeatures = activeTab === 'all' 
    ? features.all_features 
    : activeTab === 'numeric'
    ? features.numeric
    : features.categorical

  return (
    <div className="min-h-screen flex items-center justify-center px-6 pt-20">
      <div className="w-full max-w-4xl animate-fade-in">
        {/* Header */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold text-white mb-2">Select Features</h2>
          <p className="text-white/40 text-sm">
            {selectedFeatures.length} of {Object.keys(features.all_features).length} selected
          </p>
        </div>

        {/* Tabs */}
        <div className="flex justify-center space-x-2 mb-8">
          {[
            { id: 'all', label: 'All' },
            { id: 'numeric', label: 'Numeric' },
            { id: 'categorical', label: 'Categorical' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Feature grid */}
        <div className="glass-card mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-[400px] overflow-y-auto">
            {Object.entries(filteredFeatures).map(([key, value]) => (
              <div
                key={key}
                onClick={() => onFeatureSelect(key, !selectedFeatures.includes(key))}
                className={`feature-card ${selectedFeatures.includes(key) ? 'selected' : ''}`}
              >
                <div className="flex items-start space-x-3">
                  <input
                    type="checkbox"
                    checked={selectedFeatures.includes(key)}
                    onChange={() => {}}
                    className="dark-checkbox mt-0.5"
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-sm text-white truncate">{key}</span>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full ml-2 flex-shrink-0 ${
                        value.type === 'numeric' 
                          ? 'bg-indigo-500/20 text-indigo-300' 
                          : 'bg-purple-500/20 text-purple-300'
                      }`}>
                        {value.type}
                      </span>
                    </div>
                    <p className="text-xs text-white/40 line-clamp-2">{value.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action */}
        <div className="flex justify-center">
          <button
            onClick={onProceed}
            disabled={selectedFeatures.length === 0}
            className={`btn-primary ${selectedFeatures.length === 0 ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            Continue ({selectedFeatures.length})
          </button>
        </div>
      </div>
    </div>
  )
}

export default FeatureSelector
