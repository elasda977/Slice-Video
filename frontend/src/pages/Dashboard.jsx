import { useState, useEffect } from 'react'
import { videoApi } from '../api/videoApi'
import './Dashboard.css'

function Dashboard() {
  const [videos, setVideos] = useState([])
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    converting: 0,
    completed: 0,
    error: 0
  })
  const [loading, setLoading] = useState(true)
  const [serverStatus, setServerStatus] = useState(null)

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 3000) // Refresh every 3 seconds
    return () => clearInterval(interval)
  }, [])

  const loadData = async () => {
    try {
      const [videosResponse, statusResponse] = await Promise.all([
        videoApi.getVideos(),
        videoApi.getServerStatus()
      ])

      const videosList = videosResponse.data
      setVideos(videosList)
      setServerStatus(statusResponse.data)

      // Calculate statistics
      const statistics = {
        total: videosList.length,
        pending: videosList.filter(v => v.status === 'pending').length,
        converting: videosList.filter(v => v.status === 'converting').length,
        completed: videosList.filter(v => v.status === 'completed').length,
        error: videosList.filter(v => v.status === 'error').length
      }
      setStats(statistics)
    } catch (err) {
      console.error('Failed to load dashboard data:', err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      pending: 'var(--chart-pending)',
      converting: 'var(--chart-converting)',
      completed: 'var(--chart-completed)',
      error: 'var(--chart-error)'
    }
    return colors[status] || '#ccc'
  }

  const getPercentage = (count) => {
    return stats.total > 0 ? ((count / stats.total) * 100).toFixed(1) : 0
  }

  return (
    <div className="dashboard-container container">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p className="dashboard-subtitle">Real-time video conversion monitoring</p>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      ) : (
        <>
          {/* Server Status */}
          <div className="server-status-card card">
            <div className="status-header">
              <h2>Server Status</h2>
              <span className="status-indicator active">● Online</span>
            </div>
            <div className="server-stats">
              <div className="server-stat">
                <span className="stat-label">Total Videos</span>
                <span className="stat-value">{serverStatus?.videos_count || 0}</span>
              </div>
              <div className="server-stat">
                <span className="stat-label">Disk Usage</span>
                <span className="stat-value">{serverStatus?.disk_usage || '0B'}</span>
              </div>
              <div className="server-stat">
                <span className="stat-label">Active Conversions</span>
                <span className="stat-value">{stats.converting}</span>
              </div>
            </div>
          </div>

          {/* Statistics Overview */}
          <div className="stats-overview">
            <div className="stat-box card">
              <div className="stat-icon" style={{ background: 'var(--chart-pending)' }}>📝</div>
              <div className="stat-info">
                <div className="stat-number">{stats.pending}</div>
                <div className="stat-label">Pending</div>
                <div className="stat-percent">{getPercentage(stats.pending)}%</div>
              </div>
            </div>

            <div className="stat-box card">
              <div className="stat-icon" style={{ background: 'var(--chart-converting)' }}>⚙️</div>
              <div className="stat-info">
                <div className="stat-number">{stats.converting}</div>
                <div className="stat-label">Converting</div>
                <div className="stat-percent">{getPercentage(stats.converting)}%</div>
              </div>
            </div>

            <div className="stat-box card">
              <div className="stat-icon" style={{ background: 'var(--chart-completed)' }}>✅</div>
              <div className="stat-info">
                <div className="stat-number">{stats.completed}</div>
                <div className="stat-label">Completed</div>
                <div className="stat-percent">{getPercentage(stats.completed)}%</div>
              </div>
            </div>

            <div className="stat-box card">
              <div className="stat-icon" style={{ background: 'var(--chart-error)' }}>❌</div>
              <div className="stat-info">
                <div className="stat-number">{stats.error}</div>
                <div className="stat-label">Error</div>
                <div className="stat-percent">{getPercentage(stats.error)}%</div>
              </div>
            </div>
          </div>

          {/* Status Distribution Chart */}
          <div className="chart-card card">
            <h2>Status Distribution</h2>
            <div className="chart-container">
              {stats.total > 0 ? (
                <>
                  <div className="bar-chart">
                    {stats.pending > 0 && (
                      <div
                        className="bar-segment"
                        style={{
                          width: `${getPercentage(stats.pending)}%`,
                          background: 'var(--chart-pending)'
                        }}
                        title={`Pending: ${stats.pending} (${getPercentage(stats.pending)}%)`}
                      />
                    )}
                    {stats.converting > 0 && (
                      <div
                        className="bar-segment"
                        style={{
                          width: `${getPercentage(stats.converting)}%`,
                          background: 'var(--chart-converting)'
                        }}
                        title={`Converting: ${stats.converting} (${getPercentage(stats.converting)}%)`}
                      />
                    )}
                    {stats.completed > 0 && (
                      <div
                        className="bar-segment"
                        style={{
                          width: `${getPercentage(stats.completed)}%`,
                          background: 'var(--chart-completed)'
                        }}
                        title={`Completed: ${stats.completed} (${getPercentage(stats.completed)}%)`}
                      />
                    )}
                    {stats.error > 0 && (
                      <div
                        className="bar-segment"
                        style={{
                          width: `${getPercentage(stats.error)}%`,
                          background: 'var(--chart-error)'
                        }}
                        title={`Error: ${stats.error} (${getPercentage(stats.error)}%)`}
                      />
                    )}
                  </div>
                  <div className="chart-legend">
                    <div className="legend-item">
                      <span className="legend-color" style={{ background: 'var(--chart-pending)' }}></span>
                      <span>Pending ({stats.pending})</span>
                    </div>
                    <div className="legend-item">
                      <span className="legend-color" style={{ background: 'var(--chart-converting)' }}></span>
                      <span>Converting ({stats.converting})</span>
                    </div>
                    <div className="legend-item">
                      <span className="legend-color" style={{ background: 'var(--chart-completed)' }}></span>
                      <span>Completed ({stats.completed})</span>
                    </div>
                    <div className="legend-item">
                      <span className="legend-color" style={{ background: 'var(--chart-error)' }}></span>
                      <span>Error ({stats.error})</span>
                    </div>
                  </div>
                </>
              ) : (
                <div className="empty-chart">
                  <p>No videos to display</p>
                </div>
              )}
            </div>
          </div>

          {/* Real-time Video Status List */}
          <div className="video-status-card card">
            <h2>Real-time Video Status</h2>
            {videos.length === 0 ? (
              <div className="empty-state">
                <p>No videos uploaded yet</p>
              </div>
            ) : (
              <div className="video-list">
                {videos.map((video) => (
                  <div key={video.id} className="video-item">
                    <div className="video-item-header">
                      <div className="video-name">
                        <span className="video-icon">🎥</span>
                        <span>{video.name}</span>
                      </div>
                      <span
                        className={`status-badge status-${video.status}`}
                        style={{ background: getStatusColor(video.status) + '20', color: getStatusColor(video.status) }}
                      >
                        {video.status}
                      </span>
                    </div>

                    {video.status === 'converting' && (
                      <div className="conversion-progress">
                        <div className="progress-bar">
                          <div
                            className="progress-bar-fill"
                            style={{ width: `${video.progress}%` }}
                          >
                            {video.progress}%
                          </div>
                        </div>
                      </div>
                    )}

                    <div className="video-meta-info">
                      {video.duration && (
                        <span>Duration: {Math.floor(video.duration / 60)}:{(video.duration % 60).toString().padStart(2, '0')}</span>
                      )}
                      {video.segments && <span>Segments: {video.segments}</span>}
                      {video.output_size && <span>Size: {video.output_size}</span>}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

export default Dashboard
