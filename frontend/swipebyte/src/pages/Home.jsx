import React, { useState, useEffect } from 'react'
import RestaurantSwiper from '../components/RestaurantSwiper'

function Home({ isLoggedIn, token }) {
  const [restaurants, setRestaurants] = useState([])
  const [coords, setCoords] = useState({ lat: null, lon: null })
  const [groups, setGroups] = useState([])
  const [target, setTarget] = useState('self')
  const [favorites, setFavorites] = useState([])

  useEffect(() => {
    if (!token) return
    const fetchLocation = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/v1/users/', {
          headers: { Authorization: `Token ${token}` },
        })
        if (res.ok) {
          const data = await res.json()
          setCoords({ lat: data.latitude, lon: data.longitude })
        }
      } catch (err) {
        console.error(err)
      }
    }
    const fetchGroups = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/v1/groups/', {
          headers: { Authorization: `Token ${token}` },
        })
        if (res.ok) {
          const data = await res.json()
          setGroups(data)
        }
      } catch (err) {
        console.error(err)
      }
    }
    fetchLocation()
    fetchGroups()
  }, [token])

    useEffect(() => {
    if (!token) return
    const fetchFavorites = async () => {
      try {
        const url = new URL('http://localhost:8000/api/v1/favorites')
        if (target !== 'self') {
          url.searchParams.append('group', target)
        }
        const res = await fetch(url, {
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
    fetchFavorites()
  }, [token, target])

  const sortRestaurants = (list) => {
    return [...list].sort((a, b) => {
      const aFav = favorites.some((f) => f.restaurant === a.name)
      const bFav = favorites.some((f) => f.restaurant === b.name)
      return bFav - aFav
    })
  }


  const handleSearch = async (e) => {
    e.preventDefault()
    const distance = e.target.distance.value
    const price = e.target.price.value
    const paramsObj = { distance, price }
    if (coords.lat != null && coords.lon != null) {
      paramsObj.lat = coords.lat
      paramsObj.lon = coords.lon
    }
    const params = new URLSearchParams(paramsObj)
    const res = await fetch(
      `http://localhost:8000/api/v1/restaurants/?${params.toString()}`,
      {
        headers: { Authorization: `Token ${token}` },
      },
    )
    const data = await res.json()
    setRestaurants(sortRestaurants(data))
  }

  useEffect(() => {
    setRestaurants((prev) => sortRestaurants(prev))
  }, [favorites])

  const handleFavoriteToggle = async (restaurant) => {
    const existing = favorites.find((f) => f.restaurant === restaurant.name)
    if (existing) {
      await fetch(`http://localhost:8000/api/v1/favorites/${existing.id}/`, {
        method: 'DELETE',
        headers: { Authorization: `Token ${token}` },
      })
      setFavorites(favorites.filter((f) => f.id !== existing.id))
    } else {
      const body = { restaurant: restaurant.name, review: '' }
      if (target !== 'self') {
        body.group_favorites_id = target
      }
      const res = await fetch('http://localhost:8000/api/v1/favorites/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(body),
      })
      if (res.ok) {
        const newFav = await res.json()
        setFavorites([...favorites, newFav])
      }
    }
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
            <div className="col-md-4">
              <select
                name="distance"
                className="form-select"
                defaultValue="15"
              >
                <option value="15">15 miles</option>
                <option value="20">20 miles</option>
                <option value="30">30 miles</option>
                <option value="35">35 miles</option>
              </select>
            </div>
            <div className="col-md-3">
              <input
                type="text"
                name="price"
                className="form-control"
                placeholder="Price levels (1-4)"
              />
            </div>
            <div className="col-md-3">
              <select
                className="form-select"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
              >
                <option value="self">Swipe for yourself</option>
                {groups.map((g) => (
                  <option key={g.id} value={g.id}>
                    {g.group_name}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-2 d-grid">
              <button type="submit" className="btn btn-primary">
                Search
              </button>
            </div>
          </form>
          <RestaurantSwiper
            restaurants={restaurants}
            favorites={favorites}
            onLike={() => {}}
            onFavoriteToggle={handleFavoriteToggle}
          />
        </>
      )}
    </div>
  )
}

export default Home