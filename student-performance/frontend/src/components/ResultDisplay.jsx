const ResultDisplay = ({ prediction, selectedFeatures, formData, onReset }) => {
  const { prediction: score, confidence, min_score, max_score } = prediction

  const getPerformanceLevel = (score) => {
    if (score >= 15) return { label: 'Excellent', color: 'text-emerald-400' }
    if (score >= 12) return { label: 'Good', color: 'text-blue-400' }
    if (score >= 10) return { label: 'Average', color: 'text-yellow-400' }
    if (score >= 7) return { label: 'Below Average', color: 'text-orange-400' }
    return { label: 'Needs Support', color: 'text-red-400' }
  }

  const performance = getPerformanceLevel(score)
  const gaugePercentage = ((score - min_score) / (max_score - min_score)) * 100

  return (
    <div className="min-h-screen flex items-center justify-center px-6 pt-20">
      <div className="w-full max-w-md animate-scale-in">
        {/* Header */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold text-white mb-2">Prediction Result</h2>
          <p className="text-white/40 text-sm">Based on {selectedFeatures.length} features</p>
        </div>

        {/* Result Card */}
        <div className="glass-card glow-border text-center mb-6">
          {/* Score Circle */}
          <div className="relative w-48 h-48 mx-auto mb-6">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              {/* Background ring */}
              <circle
                cx="50"
                cy="50"
                r="42"
                stroke="rgba(255,255,255,0.05)"
                strokeWidth="6"
                fill="none"
              />
              {/* Progress ring */}
              <circle
                cx="50"
                cy="50"
                r="42"
                stroke="url(#resultGradient)"
                strokeWidth="6"
                fill="none"
                strokeLinecap="round"
                strokeDasharray={`${gaugePercentage * 2.64} 264`}
                className="transition-all duration-1000 ease-out"
              />
              <defs>
                <linearGradient id="resultGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#6366f1" />
                  <stop offset="100%" stopColor="#a855f7" />
                </linearGradient>
              </defs>
            </svg>
            
            {/* Score */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-bold text-white">{score}</span>
              <span className="text-sm text-white/40">/ {max_score}</span>
            </div>
          </div>

          {/* Performance Badge */}
          <div className={`text-lg font-semibold mb-4 ${performance.color}`}>
            {performance.label}
          </div>

          {/* Confidence */}
          <div className="mb-4">
            <div className="flex items-center justify-between text-xs mb-2">
              <span className="text-white/40">Confidence</span>
              <span className="text-white/60">{Math.round(confidence * 100)}%</span>
            </div>
            <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-700"
                style={{ width: `${confidence * 100}%` }}
              />
            </div>
          </div>
        </div>

        {/* Summary Card */}
        <div className="glass-card mb-6">
          <div className="grid grid-cols-2 gap-3">
            {Object.entries(formData).map(([key, value]) => (
              <div key={key} className="flex justify-between items-center py-2 px-3 bg-white/5 rounded-lg">
                <span className="text-xs text-white/40">{key}</span>
                <span className="text-sm text-white font-medium">{String(value)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Action */}
        <button
          onClick={onReset}
          className="btn-primary w-full"
        >
          New Prediction
        </button>
      </div>
    </div>
  )
}

export default ResultDisplay
