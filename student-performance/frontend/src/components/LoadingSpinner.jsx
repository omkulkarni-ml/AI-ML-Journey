const LoadingSpinner = () => {
  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50">
      <div className="text-center">
        <div className="relative w-12 h-12">
          <div className="absolute inset-0 border-2 border-white/10 rounded-full"></div>
          <div className="absolute inset-0 border-2 border-transparent border-t-indigo-500 border-r-purple-500 rounded-full animate-spin"></div>
        </div>
        <p className="text-white/50 text-sm mt-4">Processing...</p>
      </div>
    </div>
  )
}

export default LoadingSpinner
