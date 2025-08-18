import React, { useState } from 'react'

function Signup({ onAuth, backendUrl }) {
  const [form, setForm] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
  })
  const [error, setError] = useState(null)
  const [passwordCheck, setPasswordCheck] = useState({
  length: false,
  upper: false,
  lower: false,
  number: false,
  special: false,
  })

  const handlePasswordChange = (e) => {
    const password = e.target.value
    setForm({ ...form, password })
    setPasswordCheck({
      length: password.length >= 8,
      upper: /[A-Z]/.test(password),
      lower: /[a-z]/.test(password),
      number: /[0-9]/.test(password),
      special: /[^A-Za-z0-9]/.test(password),
    })
  }


  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch(`${backendUrl}/signup/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      const data = await res.json()
      if (res.ok) {
        onAuth(data.token)
              } else {
        setError(data.error || data.detail || 'Signup failed')
      }
    } catch (err) {
      console.error(err)
      setError('An error occurred. Please try again.')

    }
  }

  return (
    <div className="container mt-4">
            <div className="row justify-content-center">
        <div className="col-12 col-sm-8 col-md-6">
          <h2 className="text-center">Create Account</h2>
          {error && <div className="alert alert-danger">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                name="email"
                value={form.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Password</label>
              <input
                type="password"
                className="form-control"
                name="password"
                value={form.password}
                onChange={handlePasswordChange}
                required
              />
              <ul className="password-requirements mt-2">
                <li className={passwordCheck.length ? 'text-success' : 'text-danger'}>
                  At least 8 characters
                </li>
                <li className={passwordCheck.upper ? 'text-success' : 'text-danger'}>
                  One uppercase letter
                </li>
                <li className={passwordCheck.lower ? 'text-success' : 'text-danger'}>
                  One lowercase letter
                </li>
                <li className={passwordCheck.number ? 'text-success' : 'text-danger'}>
                  One number
                </li>
                <li className={passwordCheck.special ? 'text-success' : 'text-danger'}>
                  One special character
                </li>
              </ul>
            </div>
            <div className="mb-3">
              <label className="form-label">First Name</label>
              <input
                type="text"
                className="form-control"
                name="first_name"
                value={form.first_name}
                onChange={handleChange}
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Last Name</label>
              <input
                type="text"
                className="form-control"
                name="last_name"
                value={form.last_name}
                onChange={handleChange}
              />
            </div>
            <button type="submit" className="btn btn-primary w-100">
              Sign Up
            </button>
          </form>
        </div>
         </div>
    </div>
  )
  }

export default Signup