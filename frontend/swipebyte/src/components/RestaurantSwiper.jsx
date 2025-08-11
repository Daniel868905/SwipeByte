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
  const [animating, setAnimating] = useState(false)
  const [direction, setDirection] = useState('')
  const [action, setAction] = useState(null)

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
    setDirection('right')
    setAction('like')
    setAnimating(true)
  }

  const handleDislike = () => {
    setDirection('left')
    setAction('dislike')
    setAnimating(true)
  }

  const handleAnimationEnd = () => {
    if (action === 'like') {
      if (onLike) {
        onLike(current)
      }
      setIndex((i) => i + 1)
    } else if (action === 'dislike') {
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
    setAnimating(false)
    setDirection('')
    setAction(null)

  }

  const handleFavorite = () => {
    onFavoriteToggle(current)
  }


  return (
    <div
      className={`card mx-auto pastel-card swipe-card ${
        animating ? `swipe-${direction}` : ''
      }`}
      style={{ width: '18rem' }}
      onAnimationEnd={handleAnimationEnd}
    >

      {current.image_url && (
        <img
          src={current.image_url}
          className="card-img-top"
          alt={current.name}
          style={{ height: '200px', objectFit: 'cover' }}
        />
      )}
      <div className="card-body text-center">
        <h5 className="card-title">{current.name}</h5>
        <p className="card-text">
          {current.price || 'N/A'} | Rating: {current.rating || 'N/A'}
        </p>
        <div className="d-flex justify-content-around">
          <button className="btn btn-dislike" onClick={handleDislike}>
            Dislike
          </button>
          <button className="btn btn-favorite" onClick={handleFavorite}>
            {isFavorite ? 'Unfavorite' : 'Favorite'}
          </button>
          <button className="btn btn-like" onClick={handleLike}>
            Like
          </button>
        </div>
      </div>
    </div>
  )
}

export default RestaurantSwiper