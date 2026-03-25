/**
 * Onboarding Flow Component
 * Guides new users through setup
 */
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { BookOpen, GraduationCap, Building2, CheckCircle, ChevronRight, ChevronLeft } from 'lucide-react'
import useAuthStore from '../../store/authStore'

const steps = [
  {
    id: 0,
    title: 'Welcome!',
    description: 'Let\'s get you set up with Student Performance Predictor',
    icon: BookOpen
  },
  {
    id: 1,
    title: 'Your Role',
    description: 'Tell us about your role in education',
    icon: GraduationCap
  },
  {
    id: 2,
    title: 'Institution',
    description: 'Add your institution details',
    icon: Building2
  },
  {
    id: 3,
    title: 'All Set!',
    description: 'You\'re ready to start predicting',
    icon: CheckCircle
  }
]

const OnboardingFlow = () => {
  const [currentStep, setCurrentStep] = useState(0)
  const [formData, setFormData] = useState({
    role: 'student',
    institution: '',
    department: ''
  })
  const { updateOnboarding, user } = useAuthStore()
  const navigate = useNavigate()

  const handleNext = async () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      // Complete onboarding
      await updateOnboarding({
        step: 3,
        completed: true,
        institution: formData.institution,
        department: formData.department
      })
      navigate('/dashboard')
    }
  }

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleSkip = async () => {
    await updateOnboarding({
      step: 3,
      completed: true
    })
    navigate('/dashboard')
  }

  const updateFormData = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const CurrentStepIcon = steps[currentStep].icon

  return (
    <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className={`flex items-center justify-center w-10 h-10 rounded-full text-sm font-medium transition-all ${
                  index <= currentStep
                    ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                    : 'bg-white/10 text-gray-500'
                }`}
              >
                {index < currentStep ? (
                  <CheckCircle className="w-5 h-5" />
                ) : (
                  index + 1
                )}
              </div>
            ))}
          </div>
          <div className="h-1 bg-white/10 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-blue-500 to-purple-600"
              initial={{ width: 0 }}
              animate={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        {/* Content Card */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8"
          >
            {/* Step Header */}
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/20 to-purple-600/20 mb-4">
                <CurrentStepIcon className="w-8 h-8 text-blue-400" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">
                {steps[currentStep].title}
              </h2>
              <p className="text-gray-400">{steps[currentStep].description}</p>
            </div>

            {/* Step Content */}
            <div className="mb-8">
              {currentStep === 0 && (
                <div className="text-center space-y-4">
                  <p className="text-gray-300">
                    Welcome, <span className="text-white font-medium">{user?.first_name}</span>!
                  </p>
                  <p className="text-gray-400 text-sm">
                    Student Performance Predictor helps you understand and predict student outcomes
                    using machine learning. Let's personalize your experience.
                  </p>
                </div>
              )}

              {currentStep === 1 && (
                <div className="space-y-4">
                  <p className="text-gray-400 text-sm mb-4">Select your role:</p>
                  <div className="grid grid-cols-3 gap-4">
                    {['student', 'teacher', 'admin'].map((role) => (
                      <button
                        key={role}
                        onClick={() => updateFormData('role', role)}
                        className={`p-4 rounded-xl border transition-all ${
                          formData.role === role
                            ? 'border-blue-500 bg-blue-500/10'
                            : 'border-white/10 bg-white/5 hover:bg-white/10'
                        }`}
                      >
                        <GraduationCap className={`w-6 h-6 mx-auto mb-2 ${
                          formData.role === role ? 'text-blue-400' : 'text-gray-500'
                        }`} />
                        <span className={`text-sm font-medium capitalize ${
                          formData.role === role ? 'text-white' : 'text-gray-400'
                        }`}>
                          {role}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {currentStep === 2 && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Institution (Optional)
                    </label>
                    <input
                      type="text"
                      value={formData.institution}
                      onChange={(e) => updateFormData('institution', e.target.value)}
                      className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                      placeholder="e.g., Stanford University"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Department (Optional)
                    </label>
                    <input
                      type="text"
                      value={formData.department}
                      onChange={(e) => updateFormData('department', e.target.value)}
                      className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                      placeholder="e.g., Computer Science"
                    />
                  </div>
                </div>
              )}

              {currentStep === 3 && (
                <div className="text-center space-y-4">
                  <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-green-500/20 mb-4">
                    <CheckCircle className="w-10 h-10 text-green-400" />
                  </div>
                  <p className="text-gray-300">
                    You're all set! You can now start using the Student Performance Predictor.
                  </p>
                  <div className="bg-white/5 rounded-xl p-4 text-left">
                    <p className="text-sm text-gray-400 mb-2">Your setup:</p>
                    <ul className="space-y-1 text-sm text-gray-300">
                      <li>• Role: <span className="text-white capitalize">{formData.role}</span></li>
                      {formData.institution && (
                        <li>• Institution: <span className="text-white">{formData.institution}</span></li>
                      )}
                      {formData.department && (
                        <li>• Department: <span className="text-white">{formData.department}</span></li>
                      )}
                    </ul>
                  </div>
                </div>
              )}
            </div>

            {/* Navigation */}
            <div className="flex items-center justify-between">
              <button
                onClick={handleBack}
                disabled={currentStep === 0}
                className="flex items-center gap-2 px-4 py-2 text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronLeft className="w-5 h-5" />
                Back
              </button>

              <div className="flex items-center gap-4">
                {currentStep < steps.length - 1 && (
                  <button
                    onClick={handleSkip}
                    className="text-sm text-gray-400 hover:text-white transition-colors"
                  >
                    Skip for now
                  </button>
                )}
                <button
                  onClick={handleNext}
                  className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all transform hover:scale-[1.02] active:scale-[0.98]"
                >
                  {currentStep === steps.length - 1 ? 'Get Started' : 'Continue'}
                  <ChevronRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}

export default OnboardingFlow
