import { useState, useEffect } from 'react'
import { videoApi } from '../api/videoApi'
import './Manage.css'

function Manage() {
  const [videos, setVideos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [serverStatus, setServerStatus] = useState(null)

  useEffect(() => {
    loadVideos()
    loadServerStatus()
  }, [])

  const loadVideos = async () => {
    try {
      const response = await videoApi.getVideos()
      setVideos(response.data)
    } catch (err) {
      setError('Failed to load videos')
    } finally {
      setLoading(false)
    }
  }

  const loadServerStatus = async () => {
    try {
      const response = await videoApi.getServerStatus()
      setServerStatus(response.data)
    } catch (err) {
      console.error('Failed to load server status:', err)
    }
  }

  const handleDelete = async (video) => {
    if (!window.confirm(`Are you sure you want to delete "${video.name}"?`)) {
      return
    }

    try {
      await videoApi.deleteVideo(video.id)
      setMessage(`Deleted "${video.name}" successfully`)
      loadVideos()
      loadServerStatus()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete video')
    }
  }

  const handleCleanupAll = async () => {
    if (!window.confirm('Are you sure you want to delete ALL videos? This cannot be undone!')) {
      return
    }

    try {
      await videoApi.cleanupAll()
      setMessage('All videos deleted successfully')
      loadVideos()
      loadServerStatus()
    } catch (err) {
      setError('Failed to cleanup videos')
    }
  }

  const getStatusBadge = (status) => {
    const badges = {
      pending: 'status-badge status-pending',
      converting: 'status-badge status-converting',
      completed: 'status-badge status-completed',
      error: 'status-badge status-error',
    }
    return badges[status] || 'status-badge'
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
  }

  return (
    <div className="manage-container container">
      <div className="manage-header">
        <div>
          <h1>Manage Videos</h1>
          <p className="page-subtitle">View and manage your video library</p>
        </div>
        <button onClick={handleCleanupAll} className="btn btn-danger">
          Delete All
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {message && <div className="alert alert-success">{message}</div>}

      {serverStatus && (
        <div className="stats-overview grid grid-3">
          <div className="stat-box card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <div className="stat-label">Total Videos</div>
              <div className="stat-number">{serverStatus.videos_count}</div>
            </div>
          </div>

          <div className="stat-box card">
            <div className="stat-icon">💾</div>
            <div className="stat-content">
              <div className="stat-label">Disk Usage</div>
              <div className="stat-number">{serverStatus.disk_usage}</div>
            </div>
          </div>

          <div className="stat-box card">
            <div className="stat-icon">✓</div>
            <div className="stat-content">
              <div className="stat-label">Server Status</div>
              <div className="stat-number">{serverStatus.status}</div>
            </div>
          </div>
        </div>
      )}

      <div className="videos-card card">
        <h2>Video Library</h2>

        {loading ? (
          <div className="loading">Loading videos...</div>
        ) : videos.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📹</div>
            <h3>No videos yet</h3>
            <p>Upload and convert some videos to see them here</p>
          </div>
        ) : (
          <div className="videos-table">
            <div className="table-header">
              <div className="col-name">Name</div>
              <div className="col-status">Status</div>
              <div className="col-segments">Segments</div>
              <div className="col-size">Size</div>
              <div className="col-date">Created</div>
              <div className="col-actions">Actions</div>
            </div>

            {videos.map((video) => (
              <div key={video.id} className="table-row">
                <div className="col-name">
                  <div className="video-name">{video.name}</div>
                  <div className="video-filename">{video.original_filename}</div>
                </div>
                <div className="col-status">
                  <span className={getStatusBadge(video.status)}>
                    {video.status}
                  </span>
                  {video.status === 'converting' && (
                    <div className="progress-mini">
                      <div
                        className="progress-mini-fill"
                        style={{ width: `${video.progress}%` }}
                      />
                    </div>
                  )}
                </div>
                <div className="col-segments">{video.segments || '-'}</div>
                <div className="col-size">{video.output_size || '-'}</div>
                <div className="col-date">{formatDate(video.created_at)}</div>
                <div className="col-actions">
                  <button
                    onClick={() => handleDelete(video)}
                    className="btn btn-danger btn-small"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Manage
