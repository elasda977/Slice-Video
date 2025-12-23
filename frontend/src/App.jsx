import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import ErrorBoundary from './components/ErrorBoundary'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Convert from './pages/Convert'
import Player from './pages/Player'
import Manage from './pages/Manage'
import Upload from './pages/Upload'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <div className="app">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/convert" element={<Convert />} />
            <Route path="/player" element={<Player />} />
            <Route path="/manage" element={<Manage />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </div>
      </Router>
    </ErrorBoundary>
  )
}

export default App
