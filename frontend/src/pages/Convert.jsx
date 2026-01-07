import { useState, useEffect, useCallback } from 'react'
import { videoApi } from '../api/videoApi'
import './Convert.css'

function Convert() {
  const [selectedVideo, setSelectedVideo] = useState('')
  const [segmentDuration, setSegmentDuration] = useState(6)
  const [converting, setConverting] = useState(false)
  const [progress, setProgress] = useState(null)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    loadInputVideos()
  }, [])

  const loadInputVideos = async () => {
    try {
      // In a real scenario, you'd need an endpoint to list input directory files
      // For now, this is a placeholder
      setMessage('Upload a video first, then select it here to convert')
    } catch (err) {
      setError('Failed to load videos')
    }
  }

  const fetchProgress = useCallback(async () => {
    try {
      const videoName = selectedVideo.replace(/\.[^/.]+$/, '') // Remove extension
      const response = await videoApi.getProgress(videoName)
      setProgress(response.data)

      if (response.data.status === 'completed') {
        setConverting(false)
        setMessage('Conversion completed successfully!')
        setProgress(null)
      } else if (response.data.status === 'error') {
        setConverting(false)
        setError(response.data.message || 'Conversion failed')
        setProgress(null)
      }
    } catch (err) {
      // Progress file might not exist yet
      if (err.response?.status !== 404) {
        console.error('Failed to fetch progress:', err)
      }
    }
  }, [selectedVideo])

  useEffect(() => {
    if (converting && selectedVideo) {
      const interval = setInterval(() => {
        fetchProgress()
      }, 500) // Poll every 500ms

      return () => clearInterval(interval)
    }
  }, [converting, selectedVideo, fetchProgress])

  const handleConvert = async () => {
    if (!selectedVideo) {
      setError('Please select a video file')
      return
    }

    setConverting(true)
    setError('')
    setMessage('')
    setProgress(null)

    try {
      await videoApi.convertVideo(selectedVideo, segmentDuration)
      setMessage('Conversion started...')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start conversion')
      setConverting(false)
    }
  }

  const handleCancel = async () => {
    try {
      const videoName = selectedVideo.replace(/\.[^/.]+$/, '')
      await videoApi.cancelConversion(videoName)
      setConverting(false)
      setProgress(null)
      setMessage('Conversion cancelled')
    } catch (err) {
      setError('Failed to cancel conversion')
    }
  }

  return (
    <div className="convert-container container">
      <h1>Convert Video to HLS</h1>
      <p className="page-subtitle">Select a video and configure conversion settings</p>

      {error && <div className="alert alert-error">{error}</div>}
      {message && <div className="alert alert-success">{message}</div>}

      <div className="convert-card card">
        <div className="form-group">
          <label htmlFor="video-select">Video File Name</label>
          <input
            type="text"
            id="video-select"
            className="input"
            placeholder="Enter video filename (e.g., myvideo.mp4)"
            value={selectedVideo}
            onChange={(e) => setSelectedVideo(e.target.value)}
            disabled={converting}
          />
          <small className="form-hint">
            Enter the filename of a video in the input/ directory or that you just uploaded
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="segment-duration">Segment Duration (seconds)</label>
          <input
            type="number"
            id="segment-duration"
            className="input"
            min="1"
            max="30"
            value={segmentDuration}
            onChange={(e) => setSegmentDuration(parseInt(e.target.value))}
            disabled={converting}
          />
          <small className="form-hint">
            Recommended: 6-10 seconds. Shorter = better download protection, longer = fewer files
          </small>
        </div>

        <div className="convert-actions">
          {!converting ? (
            <button onClick={handleConvert} className="btn btn-primary">
              Start Conversion
            </button>
          ) : (
            <button onClick={handleCancel} className="btn btn-danger">
              Cancel Conversion
            </button>
          )}
        </div>
      </div>

      {progress && (
        <div className="progress-card card">
          <h2>Conversion Progress</h2>

          <div className="progress-bar">
            <div
              className="progress-bar-fill"
              style={{ width: `${progress.progress}%` }}
            >
              {progress.progress}%
            </div>
          </div>

          <div className="stats-grid grid grid-3">
            <div className="stat-card">
              <div className="stat-label">Status</div>
              <div className="stat-value">{progress.status}</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Time</div>
              <div className="stat-value">{progress.time_string || 'N/A'}</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Speed</div>
              <div className="stat-value">{progress.speed || 'N/A'}</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">ETA</div>
              <div className="stat-value">{progress.eta || 'N/A'}</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Frame</div>
              <div className="stat-value">{progress.frame || '0'}</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Progress</div>
              <div className="stat-value">{progress.progress}%</div>
            </div>
          </div>

          {progress.message && (
            <div className="progress-message">{progress.message}</div>
          )}
        </div>
      )}

      <div className="info-card card">
        <h3>How it Works</h3>
        <ol className="info-list">
          <li>Upload a video file using the Upload page</li>
          <li>Enter the filename above (e.g., &quot;myvideo.mp4&quot;)</li>
          <li>Set the segment duration (6-10 seconds recommended)</li>
          <li>Click &quot;Start Conversion&quot; to begin</li>
          <li>Monitor real-time progress as the video is converted</li>
          <li>Once complete, play the video in the Player page</li>
        </ol>
      </div>
    </div>
  )
}

export default Convert
