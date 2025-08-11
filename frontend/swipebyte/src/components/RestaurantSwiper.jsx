import React, { useState, useEffect } from 'react'

function RestaurantSwiper({
  restaurants,
  favorites,
  onLike,
  onDislike,
  onFavoriteToggle,
}) {

  const [list, setList] = useState(restaurants)
  const [index, setIndex] = useState(0)

  useEffect(() => {
    setList(restaurants)
    setIndex(0)
  }, [restaurants])

  if (!list.length) {
    return <p className="text-center">No restaurants loaded.</p>
  }

  if (index >= list.length) {
    return <p className="text-center">No more restaurants.</p>
  }

  const current = list[index]
  const isFavorite = favorites.some((f) => f.restaurant === current.name)

  const handleLike = () => {
    if (onLike) {
      onLike(current)
    }
    setIndex((i) => i + 1)
  }

  const handleDislike = () => {
    if (onDislike) {
      onDislike(current)
    }
        setList((prev) => {
      const currentName = prev[index].name
      const before = prev.slice(0, index + 1)
      const after = prev.slice(index + 1)
      const filtered = []
      const duplicates = []
      for (const r of after) {
        if (r.name === currentName) {
          duplicates.push(r)
        } else {
          filtered.push(r)
        }
      }
      return [...before, ...filtered, ...duplicates]
    })
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