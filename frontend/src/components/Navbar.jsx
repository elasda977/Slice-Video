import { Link } from 'react-router-dom'
import './Navbar.css'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <span className="logo-icon">🎬</span>
          HLS Video Platform
        </Link>

        <div className="navbar-menu">
          <Link to="/" className="navbar-link">
            Home
          </Link>
          <Link to="/upload" className="navbar-link">
            Upload
          </Link>
          <Link to="/dashboard" className="navbar-link">
            Dashboard
          </Link>
          <Link to="/player" className="navbar-link">
            Player
          </Link>
          <Link to="/manage" className="navbar-link">
            Manage
          </Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
