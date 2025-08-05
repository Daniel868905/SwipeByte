import React, { useState } from 'react'
import RestaurantSwiper from '../components/RestaurantSwiper'

function Home({ isLoggedIn, token }) {
  const [restaurants, setRestaurants] = useState([])

  const handleSearch = async (e) => {
    e.preventDefault()
    const distance = e.target.distance.value
    const price = e.target.price.value
    const params = new URLSearchParams({ distance, price })
    const res = await fetch(
      `http://localhost:8000/api/v1/restaurants/?${params.toString()}`,
      {
        headers: { Authorization: `Token ${token}` },
      }
    )
    const data = await res.json()
    setRestaurants(data)
  }

  const handleLike = async (restaurant) => {
    await fetch('http://localhost:8000/api/v1/favorites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify({ restaurant: restaurant.name, review: '' }),
    })
  }

  return (
    <div className="container py-5">
            {!isLoggedIn && (
        <div className="p-5 mb-4 bg-body-tertiary rounded-3 text-center">
          <h1 className="display-5 fw-bold">Welcome to SwipeByte</h1>
          <p className="fs-5">Create an account or log in to start using the app.</p>
          </div>
      )}
      {isLoggedIn && (
        <>
          <form onSubmit={handleSearch} className="row g-3 mb-4">
            <div className="col-md-6">
              <input
                type="number"
                name="distance"
                className="form-control"
                placeholder="Distance (meters)"
                required
              />
            </div>
            <div className="col-md-4">
              <input
                type="text"
                name="price"
                className="form-control"
                placeholder="Price levels (1-4)"
              />
            </div>
            <div className="col-md-2 d-grid">
              <button type="submit" className="btn btn-primary">
                Search
              </button>
            </div>
          </form>
          <RestaurantSwiper restaurants={restaurants} onLike={handleLike} />
        </>
      )}
    </div>
  )
}

export default Home