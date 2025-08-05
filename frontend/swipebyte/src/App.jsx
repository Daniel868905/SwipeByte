import { useState, useEffect } from 'react'
import NavBar from './components/NavBar'
import Home from './pages/Home'
import Signup from './pages/Signup'
import Login from './pages/Login'
import './App.css'

const API_BASE ='http://localhost:8000/api/v1/users'

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('token'))
  const [view, setView] = useState('home')
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem('theme') === 'dark'
  )

  useEffect(() => {
    document.body.dataset.bsTheme = darkMode ? 'dark' : 'light'
    localStorage.setItem('theme', darkMode ? 'dark' : 'light')
  }, [darkMode])

  const toggleTheme = () => setDarkMode((prev) => !prev)

    useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }, [token])


  const handleAuth = (newToken) => {
    setToken(newToken)
    setView('home')
  }

  const handleLogout = async () => {
    if (!token) return
    try {
      await fetch(`${API_BASE}/logout/`, {
        method: 'POST',
        headers: { Authorization: `Token ${token}` },
      })
    } catch (e) {
      console.error(e)
    }
    setToken(null)
    setView('home')
  }

  let page
  if (view === 'signup') {
    page = <Signup onAuth={handleAuth} backendUrl={API_BASE} />
  } else if (view === 'login') {
    page = <Login onAuth={handleAuth} backendUrl={API_BASE} />
  } else {
    page = <Home isLoggedIn={!!token} token={token} />
  }


  return (
    <>
      <NavBar
        isLoggedIn={!!token}
        onNavigate={setView}
        onLogout={handleLogout}
        darkMode={darkMode}
        onToggleTheme={toggleTheme}
      />
      {page}
    </>
  )
}

export default App
