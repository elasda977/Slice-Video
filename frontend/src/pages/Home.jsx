import { Link } from 'react-router-dom'
import './Home.css'

function Home() {
  return (
    <div className="home">
      <div className="hero">
        <div className="hero-badge">🎬 Testing Mode Active</div>
        <h1 className="hero-title">HLS Video Platform</h1>
        <p className="hero-subtitle">
          Transform your videos into secure streaming format with real-time conversion tracking
        </p>
        <p className="hero-description">
          No login required during testing. Upload, convert, and stream your videos instantly!
        </p>
        <div className="hero-buttons">
          <Link to="/upload" className="btn btn-primary btn-large">
            <span>📤</span> Get Started
          </Link>
          <Link to="/dashboard" className="btn btn-secondary btn-large">
            <span>📊</span> View Dashboard
          </Link>
        </div>
      </div>

      <div className="welcome-section container">
        <div className="card welcome-card">
          <h2>🚀 How It Works</h2>
          <p className="welcome-intro">
            Converting your videos to HLS format is easy and fast. Follow these simple steps:
          </p>

          <div className="steps-grid">
            <div className="step-card">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Upload Your Video</h3>
                <p>Choose any video file (MP4, AVI, MKV, MOV) from your computer</p>
              </div>
            </div>

            <div className="step-card">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Automatic Conversion</h3>
                <p>Watch real-time progress as your video converts to HLS format</p>
              </div>
            </div>

            <div className="step-card">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Stream Anywhere</h3>
                <p>Play your converted video with built-in download protection</p>
              </div>
            </div>
          </div>

          <div className="features-section">
            <h3>✨ Key Features</h3>
            <div className="features-grid">
              <div className="feature-item">
                <span className="feature-icon">⚡</span>
                <span>Fast conversion with progress tracking</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🔒</span>
                <span>Download protection through segmentation</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">📱</span>
                <span>Compatible with all devices</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🎯</span>
                <span>No login required (testing mode)</span>
              </div>
            </div>
          </div>

          <div className="quick-links">
            <Link to="/upload" className="quick-link">
              <span className="quick-link-icon">📤</span>
              <div>
                <strong>Upload & Process</strong>
                <small>Start converting your video</small>
              </div>
            </Link>
            <Link to="/dashboard" className="quick-link">
              <span className="quick-link-icon">📊</span>
              <div>
                <strong>Dashboard</strong>
                <small>View statistics and status</small>
              </div>
            </Link>
            <Link to="/player" className="quick-link">
              <span className="quick-link-icon">▶️</span>
              <div>
                <strong>Play Videos</strong>
                <small>Watch converted videos</small>
              </div>
            </Link>
            <Link to="/manage" className="quick-link">
              <span className="quick-link-icon">🗂️</span>
              <div>
                <strong>Manage Videos</strong>
                <small>View and delete videos</small>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
