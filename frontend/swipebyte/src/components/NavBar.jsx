import React from 'react'

function NavBar({ isLoggedIn, onNavigate, onLogout }) {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <a className="navbar-brand" href="#" onClick={() => onNavigate('home')}>
          SwipeByte
        </a>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            {!isLoggedIn && (
              <>
                <li className="nav-item">
                  <a className="nav-link" href="#" onClick={() => onNavigate('signup')}>
                    Create Account
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" href="#" onClick={() => onNavigate('login')}>
                    Login
                  </a>
                </li>
              </>
            )}
            {isLoggedIn && (
              <li className="nav-item">
                <a className="nav-link" href="#" onClick={onLogout}>
                  Logout
                </a>
              </li>
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