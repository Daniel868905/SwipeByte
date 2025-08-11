import React, { useEffect, useState } from 'react'

function Favorites({ token }) {
  const [favorites, setFavorites] = useState([])

  const fetchFavorites = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/favorites/', {
        headers: { Authorization: `Token ${token}` },
      })
      if (res.ok) {
        const data = await res.json()
        setFavorites(data)
      }
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    if (token) {
      fetchFavorites()
    }
  }, [token])

  const toggleVisited = async (fav) => {
    try {
      await fetch(`http://localhost:8000/api/v1/favorites/${fav.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({ visited: !fav.visited }),
      })
      setFavorites(
        favorites.map((f) =>
          f.id === fav.id ? { ...f, visited: !fav.visited } : f,
        ),
      )
    } catch (err) {
      console.error(err)
    }
  }

  const removeFavorite = async (fav) => {
    try {
      await fetch(`http://localhost:8000/api/v1/favorites/${fav.id}/`, {
        method: 'DELETE',
        headers: { Authorization: `Token ${token}` },
      })    
    setFavorites(favorites.filter((f) => f.id !== fav.id))
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="container py-5">
      <h2>Your Favorites</h2>
      <ul className="list-group">
        {favorites.map((fav) => (
          <li
            key={fav.id}
            className="list-group-item d-flex justify-content-between align-items-center"
          >
            <div>
              {fav.restaurant}
              <div className="form-check form-switch d-inline-block ms-3">
                <input
                  className="form-check-input"
                  type="checkbox"
                  id={`visited-${fav.id}`}
                  checked={fav.visited}
                  onChange={() => toggleVisited(fav)}
                />
                <label
                  className="form-check-label ms-1"
                  htmlFor={`visited-${fav.id}`}
                >
                  Ate there
                </label>
              </div>
            </div>
            <button
              className="btn btn-sm btn-danger"
              onClick={() => removeFavorite(fav)}
            >
              Unfavorite
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Favorites