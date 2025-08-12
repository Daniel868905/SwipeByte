import { useState, useEffect } from 'react'
import NavBar from './components/NavBar'
import Home from './pages/Home'
import Signup from './pages/Signup'
import Login from './pages/Login'
import Group from './pages/Group'
import Groups from './pages/Groups'
import Favorites from './pages/Favorites'
import Info from './pages/Info'
import { API_BASE_URL } from './config'
import './App.css'

const USER_API = `${API_BASE_URL}/api/v1/users`

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
      await fetch(`${API_BASE_URL}/logout/`, {
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
    page = <Signup onAuth={handleAuth} backendUrl={USER_API} />
  } else if (view === 'login') {
    page = <Login onAuth={handleAuth} backendUrl={USER_API} />
  } else if (view === 'groups') {
    page = <Groups token={token} />
  } else if (view === 'group') {
    page = <Group token={token} />
  } else if (view === 'favorites') {
    page = <Favorites token={token} />
  } else if (view === 'info') {
    page = <Info token={token} backendUrl={USER_API} />
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
