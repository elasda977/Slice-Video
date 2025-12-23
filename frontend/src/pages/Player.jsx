import { useState, useEffect, useRef } from 'react'
import Hls from 'hls.js'
import { videoApi } from '../api/videoApi'
import './Player.css'

function Player() {
  const [videos, setVideos] = useState([])
  const [selectedVideo, setSelectedVideo] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const videoRef = useRef(null)
  const hlsRef = useRef(null)

  useEffect(() => {
    loadVideos()
  }, [])

  useEffect(() => {
    if (selectedVideo && videoRef.current) {
      loadVideo(selectedVideo)
    }

    return () => {
      if (hlsRef.current) {
        hlsRef.current.destroy()
      }
    }
  }, [selectedVideo])

  const loadVideos = async () => {
    try {
      const response = await videoApi.getVideos()
      const completedVideos = response.data.filter(v => v.status === 'completed')
      setVideos(completedVideos)

      if (completedVideos.length > 0) {
        setSelectedVideo(completedVideos[0])
      }
    } catch (err) {
      setError('Failed to load videos')
    } finally {
      setLoading(false)
    }
  }

  const loadVideo = (video) => {
    const videoElement = videoRef.current

    if (!videoElement) return

    // Clean up previous HLS instance
    if (hlsRef.current) {
      hlsRef.current.destroy()
    }

    const playlistUrl = `/${video.playlist_path}`

    // Check if HLS is natively supported (Safari)
    if (videoElement.canPlayType('application/vnd.apple.mpegurl')) {
      videoElement.src = playlistUrl
    } else if (Hls.isSupported()) {
      // Use HLS.js for other browsers
      const hls = new Hls({
        debug: false,
        enableWorker: true,
        lowLatencyMode: true,
      })

      hls.loadSource(playlistUrl)
      hls.attachMedia(videoElement)

      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        console.log('HLS manifest loaded')
      })

      hls.on(Hls.Events.ERROR, (event, data) => {
        console.error('HLS error:', data)
        if (data.fatal) {
          setError('Failed to load video')
        }
      })

      hlsRef.current = hls
    } else {
      setError('HLS is not supported in this browser')
    }
  }

  return (
    <div className="player-container container">
      <h1>Video Player</h1>
      <p className="page-subtitle">Play your converted HLS videos</p>

      {error && <div className="alert alert-error">{error}</div>}

      {loading ? (
        <div className="loading">Loading videos...</div>
      ) : videos.length === 0 ? (
        <div className="empty-state card">
          <div className="empty-icon">📹</div>
          <h2>No Videos Available</h2>
          <p>Convert some videos first to watch them here</p>
        </div>
      ) : (
        <>
          <div className="player-card card">
            <div className="video-wrapper">
              <video
                ref={videoRef}
                className="video-player"
                controls
                playsInline
                onContextMenu={(e) => e.preventDefault()} // Disable right-click (download protection)
              >
                Your browser does not support the video tag.
              </video>
            </div>

            {selectedVideo && (
              <div className="video-info">
                <h2>{selectedVideo.name}</h2>
                <div className="video-meta">
                  <span>Segments: {selectedVideo.segments}</span>
                  <span>Size: {selectedVideo.output_size}</span>
                  <span>
                    Duration: {selectedVideo.duration ?
                      `${Math.floor(selectedVideo.duration / 60)}:${(selectedVideo.duration % 60).toString().padStart(2, '0')}`
                      : 'N/A'}
                  </span>
                </div>
              </div>
            )}
          </div>

          <div className="playlist-card card">
            <h3>Video Library</h3>
            <div className="playlist">
              {videos.map((video) => (
                <div
                  key={video.id}
                  className={`playlist-item ${selectedVideo?.id === video.id ? 'active' : ''}`}
                  onClick={() => setSelectedVideo(video)}
                >
                  <div className="playlist-item-icon">▶️</div>
                  <div className="playlist-item-info">
                    <div className="playlist-item-title">{video.name}</div>
                    <div className="playlist-item-meta">
                      {video.segments} segments • {video.output_size}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="info-card card">
            <h3>Download Protection</h3>
            <p>
              This video is segmented into multiple small files (.ts segments) for streaming.
              Right-click download is disabled to prevent easy downloading of the full video.
              This provides moderate protection against casual downloading while maintaining
              compatibility with all browsers through HLS (HTTP Live Streaming) technology.
            </p>
          </div>
        </>
      )}
    </div>
  )
}

export default Player
