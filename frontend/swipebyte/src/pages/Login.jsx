import React, { useState } from 'react'

function Login({ onAuth, backendUrl }) {
   const [form, setForm] = useState({ email: '', password: '' })
  const [token, setToken] = useState(null)
  const [address, setAddress] = useState('')
  const [needsLocation, setNeedsLocation] = useState(false)
  const googleApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${backendUrl}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (res.ok) {
        const data = await res.json()
               navigator.geolocation.getCurrentPosition(
          async (pos) => {
            await fetch(`${backendUrl}/location/`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Token ${data.token}`,
              },
              body: JSON.stringify({
                latitude: pos.coords.latitude,
                longitude: pos.coords.longitude,
              }),
            })
            onAuth(data.token)
          },
          () => {
            setToken(data.token)
            setNeedsLocation(true)
          }
        )
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleAddressSubmit = async () => {
    if (!address) return
    try {
      const res = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(
          address
        )}&key=${googleApiKey}`
      )
      const geo = await res.json()
      const loc = geo.results[0]?.geometry?.location
      if (loc) {
        await fetch(`${backendUrl}/location/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`,
          },
          body: JSON.stringify({ latitude: loc.lat, longitude: loc.lng }),
        })
        onAuth(token)
      }
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="container mt-4">
      <h2>Login</h2>
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
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Login
        </button>
      </form>
            {needsLocation && (
        <div className="mt-3">
          <label className="form-label">Enter your location</label>
          <input
            type="text"
            className="form-control"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            placeholder="Address"
          />
          <button
            type="button"
            className="btn btn-secondary mt-2"
            onClick={handleAddressSubmit}
          >
            Use Address
          </button>
        </div>
      )}
    </div>
  )
}

export default Login