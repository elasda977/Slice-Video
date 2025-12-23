import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { videoApi } from '../api/videoApi'
import './Upload.css'

function Upload() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [converting, setConverting] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [conversionProgress, setConversionProgress] = useState(0)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [currentStep, setCurrentStep] = useState('idle') // idle, uploading, converting, completed

  const navigate = useNavigate()

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      // Validate file type
      const validTypes = ['video/mp4', 'video/x-msvideo', 'video/x-matroska', 'video/quicktime']
      if (!validTypes.includes(selectedFile.type) && !selectedFile.name.match(/\.(mp4|avi|mkv|mov)$/i)) {
        setError('Please select a valid video file (MP4, AVI, MKV, MOV)')
        setFile(null)
        return
      }

      setFile(selectedFile)
      setError('')
      setMessage('')
      setCurrentStep('idle')
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first')
      return
    }

    setError('')
    setMessage('')

    // Step 1: Upload
    setUploading(true)
    setCurrentStep('uploading')
    setMessage('Uploading video...')

    try {
      const uploadResponse = await videoApi.uploadVideo(file, (progress) => {
        setUploadProgress(progress)
      })

      setUploading(false)
      setUploadProgress(100)
      setMessage('Upload complete! Starting conversion...')

      // Step 2: Auto-convert with default 6-second segments
      setCurrentStep('converting')
      setConverting(true)

      const conversionResponse = await videoApi.convertVideo(file.name, 6)
      const videoName = conversionResponse.data.video_name

      // Step 3: Monitor conversion progress
      monitorConversion(videoName)

    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
      setUploadProgress(0)
      setUploading(false)
      setConverting(false)
      setCurrentStep('idle')
    }
  }

  const monitorConversion = (videoName) => {
    const interval = setInterval(async () => {
      try {
        const response = await videoApi.getProgress(videoName)
        const progress = response.data

        setConversionProgress(progress.progress || 0)

        if (progress.status === 'completed') {
          clearInterval(interval)
          setConverting(false)
          setCurrentStep('completed')
          setMessage('Video processed successfully! Redirecting to dashboard...')

          // Redirect to dashboard after 2 seconds
          setTimeout(() => {
            navigate('/dashboard')
          }, 2000)
        } else if (progress.status === 'error') {
          clearInterval(interval)
          setConverting(false)
          setCurrentStep('idle')
          setError('Conversion failed: ' + (progress.message || 'Unknown error'))
        }
      } catch (err) {
        // Progress file might not exist yet, continue polling
        if (err.response?.status !== 404) {
          console.error('Failed to fetch progress:', err)
        }
      }
    }, 1000) // Poll every second for smoother updates
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  return (
    <div className="upload-container container">
      <h1>Upload Video</h1>
      <p className="page-subtitle">Upload your video - it will be automatically processed for streaming</p>

      <div className="upload-card card">
        {error && <div className="alert alert-error">{error}</div>}
        {message && <div className="alert alert-success">{message}</div>}

        {/* Progress Steps Indicator */}
        <div className="steps-indicator">
          <div className={`step ${currentStep === 'uploading' || currentStep === 'converting' || currentStep === 'completed' ? 'active' : ''} ${currentStep === 'converting' || currentStep === 'completed' ? 'completed' : ''}`}>
            <div className="step-number">1</div>
            <div className="step-label">Upload</div>
          </div>
          <div className="step-line"></div>
          <div className={`step ${currentStep === 'converting' || currentStep === 'completed' ? 'active' : ''} ${currentStep === 'completed' ? 'completed' : ''}`}>
            <div className="step-number">2</div>
            <div className="step-label">Process</div>
          </div>
          <div className="step-line"></div>
          <div className={`step ${currentStep === 'completed' ? 'active completed' : ''}`}>
            <div className="step-number">3</div>
            <div className="step-label">Ready</div>
          </div>
        </div>

        <div className="upload-area">
          <input
            type="file"
            id="file-input"
            accept="video/mp4,video/x-msvideo,video/x-matroska,video/quicktime,.mp4,.avi,.mkv,.mov"
            onChange={handleFileChange}
            disabled={uploading || converting}
            style={{ display: 'none' }}
          />
          <label htmlFor="file-input" className="file-label">
            <div className="upload-icon">📁</div>
            <div className="upload-text">
              {file ? file.name : 'Click to select a video file'}
            </div>
            {file && (
              <div className="file-info">
                Size: {formatFileSize(file.size)}
              </div>
            )}
          </label>
        </div>

        {/* Upload Progress */}
        {uploading && (
          <div className="upload-progress">
            <h4>Step 1: Uploading Video</h4>
            <div className="progress-bar">
              <div
                className="progress-bar-fill"
                style={{ width: `${uploadProgress}%` }}
              >
                {uploadProgress}%
              </div>
            </div>
            <p className="progress-text">Uploading to server... {uploadProgress}%</p>
          </div>
        )}

        {/* Conversion Progress */}
        {converting && (
          <div className="conversion-progress">
            <h4>Step 2: Processing Video</h4>
            <div className="progress-bar">
              <div
                className="progress-bar-fill"
                style={{ width: `${conversionProgress}%` }}
              >
                {conversionProgress}%
              </div>
            </div>
            <p className="progress-text">Converting to streaming format... {conversionProgress}%</p>
            <p className="progress-hint">This may take a few minutes depending on video length</p>
          </div>
        )}

        <div className="upload-actions">
          <button
            onClick={handleUpload}
            className="btn btn-primary"
            disabled={!file || uploading || converting}
          >
            {uploading ? 'Uploading...' : converting ? 'Processing...' : 'Upload & Process'}
          </button>
          {file && !uploading && !converting && (
            <button
              onClick={() => {
                setFile(null)
                setError('')
                setMessage('')
                setCurrentStep('idle')
                setUploadProgress(0)
                setConversionProgress(0)
              }}
              className="btn btn-secondary"
            >
              Clear
            </button>
          )}
        </div>

        <div className="upload-info">
          <h3>How It Works</h3>
          <ul>
            <li>✅ Select your video file (MP4, AVI, MKV, MOV)</li>
            <li>✅ Click "Upload & Process" - video will be uploaded</li>
            <li>✅ Automatic conversion starts immediately</li>
            <li>✅ Video is split into 6-second segments for streaming</li>
            <li>✅ Redirects to dashboard when complete</li>
          </ul>

          <h3>Supported Formats</h3>
          <ul>
            <li>MP4 (.mp4) - Recommended</li>
            <li>AVI (.avi)</li>
            <li>MKV (.mkv)</li>
            <li>MOV (.mov)</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Upload
