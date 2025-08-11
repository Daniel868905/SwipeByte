import React, { useState } from 'react'

function RestaurantSwiper({ restaurants, favorites, onLike, onFavoriteToggle }) {
  const [index, setIndex] = useState(0)

  if (!restaurants.length) {
    return <p className="text-center">No restaurants loaded.</p>
  }

  if (index >= restaurants.length) {
    return <p className="text-center">No more restaurants.</p>
  }

  const current = restaurants[index]
  const isFavorite = favorites.some((f) => f.restaurant === current.name)

  const handleLike = () => {
    if (onLike) {
      onLike(current)
    }
    setIndex((i) => i + 1)
  }

    const handleDislike = () => {
    setIndex((i) => i + 1)
  }

  const handleFavorite = () => {
    onFavoriteToggle(current)
  }


  return (
    <div className="card mx-auto" style={{ width: '18rem' }}>
      {current.image_url && (
        <img src={current.image_url} className="card-img-top" alt={current.name} />
      )}
      <div className="card-body text-center">
        <h5 className="card-title">{current.name}</h5>
        <p className="card-text">
          {current.price || 'N/A'} | Rating: {current.rating || 'N/A'}
        </p>
        <div className="d-flex justify-content-around">
          <button className="btn btn-danger" onClick={handleDislike}>
            Dislike
          </button>
          <button
            className="btn btn-warning"
            onClick={handleFavorite}
          >
            {isFavorite ? 'Unfavorite' : 'Favorite'}
          </button>
          <button className="btn btn-success" onClick={handleLike}>
            Like
          </button>
        </div>
      </div>
    </div>
  )
}

export default RestaurantSwiper