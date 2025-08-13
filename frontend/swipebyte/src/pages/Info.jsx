import React, { useEffect, useState } from 'react'

function Info({ token, backendUrl }) {
  const [user, setUser] = useState(null)
  const [form, setForm] = useState({ old_password: '', new_password: '' })
  const [message, setMessage] = useState('')

  useEffect(() => {
    const fetchInfo = async () => {
      try {
        const res = await fetch(`${backendUrl}/`, {
          headers: { Authorization: `Token ${token}` },
        })
        if (res.ok) {
          const data = await res.json()
          setUser(data)
        }
      } catch (err) {
        console.error(err)
      }
    }
    fetchInfo()
  }, [token, backendUrl])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMessage('')
    try {
      const res = await fetch(`${backendUrl}/password/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(form),
      })
      if (res.ok) {
        setMessage('Password updated')
        setForm({ old_password: '', new_password: '' })
      } else {
        const data = await res.json()
        setMessage(data.detail || 'Error updating password')
      }
    } catch (err) {
      console.error(err)
      setMessage('Error updating password')
    }
  }


 return (
    <div className="container mt-4">
      <h2>User Info</h2>
      {user && (
        <p>
          Username: <strong>{user.username}</strong>
        </p>
      )}
      <h3>Reset Password</h3>
      <form onSubmit={handleSubmit} className="mb-3">
        <div className="mb-3">
          <label className="form-label">Old Password</label>
          <input
            type="password"
            name="old_password"
            className="form-control"
            value={form.old_password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">New Password</label>
          <input
            type="password"
            name="new_password"
            className="form-control"
            value={form.new_password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Update Password
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  )
}

export default Info