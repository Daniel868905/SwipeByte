import React, { useCallback, useEffect, useState } from 'react'

function Favorites({ token }) {
  const [favorites, setFavorites] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [selected, setSelected] = useState(null)
  const [comments, setComments] = useState([])

  const fetchFavorites = useCallback(async () => {
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
  }, [token])

  useEffect(() => {
    if (token) {
      fetchFavorites()
    }
  }, [token, fetchFavorites])

  const toggleVisited = async (fav) => {
    try {
      const newVisited = !fav.visited
      let review = fav.review
      if (newVisited) {
        review = prompt('Leave a comment', fav.review || '') || ''
      }

      await fetch(`http://localhost:8000/api/v1/favorites/${fav.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({ visited: newVisited, review }),
      })
      setFavorites(
        favorites.map((f) =>
          f.id === fav.id ? { ...f, visited: newVisited, review } : f,
        ),
      )
    } catch (err) {
      console.error(err)
    }
  }
  const openComments = async (fav) => {
    setSelected(fav)
    try {
      const res = await fetch(
        `http://localhost:8000/api/v1/favorites/?restaurant=${encodeURIComponent(
          fav.restaurant,
        )}`,
        {
          headers: { Authorization: `Token ${token}` },
        },
      )
      if (res.ok) {
        const data = await res.json()
        setComments(data)
      }
    } catch (err) {
      console.error(err)
    }
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setSelected(null)
    setComments([])
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
              <span
                role="button"
                className="text-decoration-underline"
                onClick={() => openComments(fav)}
              >
                {fav.restaurant}
              </span>
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
              className="btn btn-sm btn-dislike"
              onClick={() => removeFavorite(fav)}
            >
              Unfavorite
            </button>
          </li>
        ))}
      </ul>

      {showModal && selected && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h5>Comments for {selected.restaurant}</h5>
            <ul className="list-group">
              {comments.map((c) => (
                <li key={c.id} className="list-group-item">
                  <strong>
                    {c.user_favorites?.email || c.group_favorites?.group_name}:
                  </strong>{' '}
                  {c.review || 'No comment'}
                </li>
              ))}
            </ul>
            <button className="btn btn-secondary mt-3" onClick={closeModal}>
              Close
            </button>
          </div>
        </div>
      )}

    </div>
  )
}

export default Favorites