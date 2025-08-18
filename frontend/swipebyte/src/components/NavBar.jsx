import React, { useState } from 'react'

function NavBar({ isLoggedIn, onNavigate, onLogout, darkMode, onToggleTheme }) {
  const navbarTheme = darkMode ? 'navbar-dark bg-dark' : 'navbar-light bg-light'
  const [collapsed, setCollapsed] = useState(true)

  return (
    <nav className={`navbar navbar-expand-lg ${navbarTheme}`}>
      <div className="container-fluid">
        <a
          className="navbar-brand"
          href="#"
          onClick={(e) => {
            e.preventDefault()
            onNavigate('home')
          }}
        >
          SwipeByte
        </a>
        <button
          className={`navbar-toggler${collapsed ? ' collapsed' : ''}`}
          type="button"
          aria-controls="navbarNav"
          aria-expanded={!collapsed}
          aria-label="Toggle navigation"
          onClick={() => setCollapsed(!collapsed)}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="30"
            height="30"
            viewBox="0 0 30 30"
          >
            <path
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              d="M4 7h22M4 15h22M4 23h22"
            />
          </svg>
        </button>
        <div
          className={`collapse navbar-collapse${collapsed ? '' : ' show'}`}
          id="navbarNav"
        >
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <a
                className="nav-link"
                href="#"
                onClick={(e) => {
                  e.preventDefault()
                  onNavigate('home')
                }}
              >
                Home
              </a>
            </li>
            {!isLoggedIn && (
              <>
                <li className="nav-item">
                  <a
                    className="nav-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                      onNavigate('signup')
                    }}
                  >
                    Create Account
                  </a>
                </li>
                <li className="nav-item">
                  <a
                    className="nav-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                      onNavigate('login')
                    }}
                  >
                    Login
                  </a>
                </li>
              </>
            )}
            {isLoggedIn && (
              <>
                <li className="nav-item">
                  <a
                    className="nav-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                      onNavigate('groups')
                    }}
                  >
                    Groups
                  </a>
                </li>
                <li className="nav-item">
                  <a
                    className="nav-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                      onNavigate('favorites')
                    }}
                  >
                    Favorites
                  </a>
                </li>
                <li className="nav-item">
                  <a
                    className="nav-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                      onNavigate('group')
                    }}
                  >
                    Create Group
                  </a>
                </li>
                <li className="nav-item">
                  <a
                    className="nav-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                      onNavigate('info')
                    }}
                  >
                    Account
                  </a>
                </li>
                <li className="nav-item">
                  <a
                    className="nav-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                      onLogout()
                    }}
                  >
                    Logout
                  </a>
                </li>
              </>
            )}
            <li className="nav-item d-flex align-items-center ms-3">
              <div className="form-check form-switch m-0">
                <input
                  className="form-check-input"
                  type="checkbox"
                  role="switch"
                  id="themeSwitch"
                  checked={darkMode}
                  onChange={onToggleTheme}
                />
                <label className="form-check-label ms-2" htmlFor="themeSwitch">
                  {darkMode ? 'Dark' : 'Light'}
                </label>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  )
}

export default NavBar